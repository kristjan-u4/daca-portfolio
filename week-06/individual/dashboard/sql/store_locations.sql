WITH store_locations AS (
  SELECT
      DISTINCT(s.store_location) AS store_location
  FROM sales s
  ORDER BY s.store_location ASC NULLS LAST
)
SELECT
  COALESCE(store_location, 'Online') AS store_location
FROM store_locations;