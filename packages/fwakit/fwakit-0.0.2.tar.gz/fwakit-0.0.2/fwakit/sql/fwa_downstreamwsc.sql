CREATE OR REPLACE FUNCTION fwa_downstreamwsc(
    wscode_ltree_a ltree,
    localcode_ltree_a ltree,
    wscode_ltree_b ltree,
    localcode_ltree_b ltree
)

RETURNS boolean AS $$

SELECT
(
          -- donwstream criteria 1 - same blue line, lower measure
          (b.blue_line_key = a.blue_line_key AND
           b.downstream_route_measure <= a.downstream_route_measure)
          OR
          -- criteria 2 - watershed code a is a child of watershed code b,
          -- (but not equal, that has to be handled by the blue line)
          (b.wscode_ltree @> a.wscode_ltree
              AND b.wscode_ltree != a.wscode_ltree
              AND (
                   -- local code is lower or wscode and localcode are equivalent
                   (
                    b.localcode_ltree < subltree(a.localcode_ltree, 0, nlevel(b.localcode_ltree))
                    OR b.wscode_ltree = b.localcode_ltree
                   )
                   -- OR any missed side channels on the same watershed code
                   OR (b.wscode_ltree = a.wscode_ltree AND
                       b.blue_line_key != a.blue_line_key AND
                       b.localcode_ltree < a.localcode_ltree)
                   )
          )
      )