
--Postgresql

SELECT trip_end_location, MAX(taxi_id) from ((SELECT COUNT(*) AS taxi_id_trips, taxi_id, trip_end_location FROM moves_chicago_taxis GROUP BY taxi_id, trip_end_location) as x inner join
    (SELECT MAX(taxi_id_trips) as m, trip_end_location as p_la FROM (SELECT COUNT(*) AS taxi_id_trips, taxi_id, trip_end_location FROM moves_chicago_taxis GROUP BY taxi_id, trip_end_location) AS most_popular_taxi_id group by trip_end_location) as y
    on x.taxi_id_trips = y.m and x.trip_end_location = y.p_la) AS m_p
group by trip_end_location
order by trip_end_location;

--MonetDB

SELECT trip_end_location, max(taxi_id) as most_popular_taxi from (SELECT COUNT(*) AS taxi_id_trips, taxi_id, trip_end_location FROM moves_chicago_taxis GROUP BY taxi_id, trip_end_location) as x inner join
    (SELECT MAX(taxi_id_trips) as m, trip_end_location as t_end FROM (SELECT COUNT(*) AS taxi_id_trips, taxi_id, trip_end_location FROM moves_chicago_taxis GROUP BY taxi_id, trip_end_location) AS most_popular_taxi_id group by trip_end_location) as y
    on x.taxi_id_trips = y.m and x.trip_end_location = y.t_end
group by trip_end_location
order by trip_end_location;
