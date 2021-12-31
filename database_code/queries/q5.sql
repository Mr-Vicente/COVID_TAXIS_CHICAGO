
--What is the area with more movement on a given small period of time (15 minutes)

SELECT year, month, day, hour, minute, amount_of_trips, dropoff_centroid_location
from chicago_taxis_grid_time as c_t 
inner join date_dim as d on (c_t.trip_end_date = d.date_id)
inner join hour_dim as h on (c_t.trip_end_hour = h.hour_id)
where is_busy_hour = True and year = 2021 and month = 'september' and day = 25;

--What is the area with more movement on a certain day rushes hour

SELECT year, month, day, dropoff_centroid_location, SUM(amount_of_trips) as total_amount_of_trips
from chicago_taxis_grid_time as c_t 
inner join date_dim as d on (c_t.trip_end_date = d.date_id)
inner join hour_dim as h on (c_t.trip_end_hour = h.hour_id)
where is_busy_hour = True and year = 2020 and month = 'september' and day = 26
GROUP BY year, month, day,dropoff_centroid_location;



