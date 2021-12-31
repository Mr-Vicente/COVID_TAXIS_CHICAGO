--Postgresql

SELECT COUNT(*)/SUM(total_doses) as trip_vax_ratio, longitude,latitude FROM (select * from covid_chicago_taxis 
inner join date_dim on (date_dim.date_id = trip_end_date)
WHERE date_dim.year = 2021) as x
INNER JOIN (vaccinations 
inner JOIN location_dim on(vaccinations.location = location_dim.location_id))
ON ST_DistanceSphere(
    ST_MakePoint(trip_end_longitude,trip_end_latitude),
    ST_MakePoint(longitude,latitude)
) <= 10
inner JOIN date_dim2 on (date_dim2.date_id = vax_date)
WHERE x.year = date_dim2.year
and x.month = date_dim2.month
and x.day = date_dim2.day
GROUP BY longitude,latitude
ORDER BY trip_vax_ratio DESC
limit 10;

--MonetDB

SELECT COUNT(*)/SUM(total_doses) as trip_vax_ratio, longitude,latitude FROM (SELECT * FROM covid_chicago_taxis 
INNER JOIN date_dim on date_dim.date_id = trip_end_date
WHERE date_dim.year_ = 2021) as x
INNER JOIN (vaccinations 
INNER JOIN location_dim on vaccinations.location = location_dim.location_id)
ON ST_Distance(
    ST_MakePoint(trip_end_longitude,trip_end_latitude),
    ST_MakePoint(longitude,latitude)
) <= 10
INNER JOIN date_dim2 on date_dim2.date_id = vax_date
WHERE "and"(x.year_ = date_dim2.year_, "and"(x.month_ = date_dim2.month_, x.day_ = date_dim2.day_))
GROUP BY longitude,latitude
ORDER BY trip_vax_ratio DESC
limit 10;
