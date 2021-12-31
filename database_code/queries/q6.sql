--What is the company with more success on a given area and day

SELECT year, month, day, dropoff_centroid_location, count(most_popular_company) as company_count, most_popular_company as one_popular_company
from chicago_taxis_grid_time as c_t 
inner join date_dim as d on (c_t.trip_end_date = d.date_id)
inner join hour_dim as h on (c_t.trip_end_hour = h.hour_id)
where year = 2021 and month = 'september' and day = 25
group by year, month, day, dropoff_centroid_location, most_popular_company
order by dropoff_centroid_location, company_count desc
;

--What is the company with more success on a given area and month

SELECT year, month, dropoff_centroid_location, count(most_popular_company) as company_count, most_popular_company as one_popular_company
from chicago_taxis_grid_time as c_t 
inner join date_dim as d on (c_t.trip_end_date = d.date_id)
inner join hour_dim as h on (c_t.trip_end_hour = h.hour_id)
where year = 2021 and month = 'september' and day = 25
group by year, month, dropoff_centroid_location, most_popular_company
order by dropoff_centroid_location, company_count desc
;
