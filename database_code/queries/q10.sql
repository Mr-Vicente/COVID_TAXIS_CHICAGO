--Postgresql and MonetDB

SELECT avg_trip_total, zip_code, longitude, latitude
FROM chicago_taxis_grid inner join location_grid_dim
on (chicago_taxis_grid.trip_end_location = location_grid_dim.location_id)
ORDER BY value DESC