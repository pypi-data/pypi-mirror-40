create table watersheds.prelim_paul_cr AS
WITH prelim AS
(SELECT
          pt.station,
          wsd.waterbody_key,
          ST_Multi(ST_Force2D(wsd.geom)) as geom
        FROM watersheds.stations_referenced pt
        INNER JOIN whse_basemapping.fwa_watersheds_poly_sp wsd
        ON
          -- b is a child of a, always
          wsd.wscode_ltree <@ pt.wscode_ltree
          -- don't include the bottom watershed
        AND wsd.localcode_ltree != pt.localcode_ltree
        AND
            -- conditional upstream join logic, based on whether watershed codes are equivalent
          CASE
            -- first, consider simple case - streams where wscode and localcode are equivalent
             WHEN
                pt.wscode_ltree = pt.localcode_ltree
             THEN TRUE
             -- next, the more complicated case - where wscode and localcode are not equal
             WHEN
                pt.wscode_ltree != pt.localcode_ltree AND
                (
                 -- tributaries: b wscode > a localcode and b wscode is not a child of a localcode
                    (wsd.wscode_ltree > pt.localcode_ltree AND
                     NOT wsd.wscode_ltree <@ pt.localcode_ltree)
                    OR
                 -- capture side channels: b is the same watershed code, with larger localcode
                    (wsd.wscode_ltree = pt.wscode_ltree
                     AND wsd.localcode_ltree >= pt.localcode_ltree)
                )
              THEN TRUE
          END
      WHERE pt.station = '08LB012'),

distinct_lakes_reservoirs as (
 select distinct p.station, p.waterbody_key
 from prelim p
 inner join whse_basemapping.fwa_lakes_poly l on p.waterbody_key = l.waterbody_key
 union ALL
 select distinct p.station, p.waterbody_key
 from prelim p
 inner join whse_basemapping.fwa_manmade_waterbodies_poly l on p.waterbody_key = l.waterbody_key
),

all_lakes_reservoir_wsd_polys AS
(
  SELECT lr.station, lr.waterbody_key, ST_Multi(ST_Force2D(w.geom)) as geom
  from
  distinct_lakes_reservoirs lr
  INNER JOIN whse_basemapping.fwa_watersheds_poly_sp w
  ON lr.waterbody_key = w.waterbody_key
)

SELECT * FROM prelim
UNION
SELECT * from all_lakes_reservoir_wsd_polys


