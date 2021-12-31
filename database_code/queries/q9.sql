--Postgresql and MonetDB

SELECT count(*) as arrivals, covid_phase, trip_end_location from moves_chicago_taxis as m inner join date_dim
on(date_dim.date_id = m.trip_end_date)
GROUP BY covid_phase, trip_end_location
order by arrivals Desc;