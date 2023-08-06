
WITH stn_point AS
(SELECT
  e.station,
  e.blue_line_key,
  e.downstream_route_measure,
  s.waterbody_key,
  ST_LineInterpolatePoint(ST_LineMerge(s.geom), ROUND(CAST((e.downstream_route_measure - s.downstream_route_measure) / s.length_metre AS NUMERIC), 5)) AS geom
  FROM public.stations_referenced e
 INNER JOIN whse_basemapping.fwa_stream_networks_sp s
ON e.linear_feature_id = s.linear_feature_id
WHERE station = '08NL069'),

wsds_river_prelim AS
(SELECT
  wsd.watershed_feature_id,
  wsd.waterbody_key,
  wsd.geom
 FROM whse_basemapping.fwa_watersheds_poly_sp wsd
 INNER JOIN stn_point pt
  ON (wsd.waterbody_key = pt.waterbody_key
     AND ST_DWithin(wsd.geom, pt.geom, 100))
     ),

wsds_river AS
(SELECT DISTINCT watershed_feature_id, waterbody_key, geom
FROM (
(SELECT wsd.watershed_feature_id, wsd.waterbody_key, wsd.geom
FROM whse_basemapping.fwa_watersheds_poly_sp wsd
INNER JOIN wsds_river_prelim p ON ST_Intersects(wsd.geom, p.geom)
WHERE wsd.watershed_feature_id != p.watershed_feature_id
AND wsd.waterbody_key != 0
UNION ALL
SELECT * FROM wsds_river_prelim)
) as foo
) ,


wsds_adjacent AS
(SELECT
    r.watershed_feature_id as riv_id,
  wsd.watershed_feature_id,
  wsd.geom,
  ST_Distance(s.geom, wsd.geom) as dist_to_site
FROM whse_basemapping.fwa_watersheds_poly_sp wsd
INNER JOIN wsds_river r
ON (r.geom && wsd.geom AND ST_Relate(r.geom, wsd.geom, '****1****'))
INNER JOIN stn_point s ON ST_DWithin(s.geom, r.geom, 5)
LEFT OUTER JOIN whse_basemapping.fwa_lakes_poly lk
ON wsd.waterbody_key = lk.waterbody_key
LEFT OUTER JOIN whse_basemapping.fwa_rivers_poly riv
ON wsd.waterbody_key = riv.waterbody_key
LEFT OUTER JOIN whse_basemapping.fwa_manmade_waterbodies_poly mm
ON wsd.waterbody_key = mm.waterbody_key
WHERE lk.waterbody_key IS NULL AND riv.waterbody_key IS NULL AND mm.waterbody_key IS NULL
AND r.watershed_feature_id != wsd.watershed_feature_id
AND wsd.watershed_feature_id NOT IN (SELECT watershed_feature_id FROM wsds_river)),

wsds_adjacent_nearest AS
(SELECT DISTINCT ON (riv_id) riv_id, watershed_feature_id, dist_to_site, geom
FROM wsds_adjacent
ORDER BY riv_id, dist_to_site),

edges AS (SELECT
   w_adj.watershed_feature_id,
   ST_Difference(ST_ExteriorRing((ST_Dump(w_adj.geom)).geom), w_riv.geom ) as geom
FROM wsds_adjacent_nearest w_adj,
(SELECT ST_Union(geom) as geom FROM wsds_river) as w_riv),

cut_line_ends AS (SELECT
  row_number() over() as id,
  ST_ClosestPoint(edges.geom, stn.geom) as geom
FROM edges, stn_point stn),

blade AS (
SELECT 1 as id, ST_MakeLine(geom) geom FROM
(SELECT
  CASE WHEN id = 2 THEN 3
  ELSE id
  END AS id,
  geom
FROM cut_line_ends
UNION ALL
SELECT 2 AS id, geom FROM stn_point
ORDER BY id) as orderedpts),

to_split AS
(SELECT (ST_Dump(ST_Union(geom))).geom AS geom FROM
(SELECT geom FROM wsds_adjacent_nearest
 UNION ALL
 SELECT geom FROM wsds_river
 UNION ALL
 SELECT wsd.geom FROM whse_basemapping.fwa_watersheds_poly_sp wsd
 INNER JOIN stn_point pt
 ON ST_DWithin(wsd.geom, pt.geom, 100)
 WHERE wsd.waterbody_key != 0) AS bar)

SELECT * FROM blade
/*SELECT
  stream.station,
  'wb cut' AS source,
  ST_Multi(ST_Force2d(baz.geom)) AS geom
FROM
(SELECT
 (ST_Dump(ST_Split(ST_Snap(w.geom, b.geom, .001), b.geom))).geom
FROM to_split w, blade b) AS baz
INNER JOIN
(SELECT p.station, str.geom FROM whse_basemapping.fwa_stream_networks_sp str
 INNER JOIN stn_point p
 ON str.blue_line_key = p.blue_line_key
 AND str.downstream_route_measure > p.downstream_route_measure
 ORDER BY str. downstream_route_measure asc
 LIMIT 1) stream
 ON st_intersects(baz.geom, stream.geom)
*/