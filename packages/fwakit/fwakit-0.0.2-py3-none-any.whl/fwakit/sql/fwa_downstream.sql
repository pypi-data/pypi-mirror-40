CREATE OR REPLACE FUNCTION fwa_downstream_test
(
    blkey_a integer,
    blkey_b integer

)

RETURNS boolean AS $$

SELECT
  CASE
    -- Criteria 1 - same blue line, lower measure
    WHEN blkey_b = blkey_a THEN TRUE
    ELSE FALSE
  END

$$
language 'sql' immutable strict parallel safe;
