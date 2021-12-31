SELECT longitude,latitude, amount_of_trips FROM chicago_taxis_grid 
INNER JOIN location_grid_dim on (dropoff_centroid_location = location_id)
ORDER BY amount_of_trips DESC
LIMIT 10;

-- VS

SELECT COUNT(*) as amount_of_trips , trip_end_location as dropoff_centroid_location
FROM moves_chicago_taxis 
GROUP BY dropoff_centroid_location;