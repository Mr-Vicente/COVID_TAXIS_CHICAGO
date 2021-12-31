--Postgresql

SELECT trip_end_location, trunc(sum(trip_tips)/(sum(trip_seconds)/60/60),2) as tip_hour_rate, sum(trip_seconds) as total_seconds, sum(trip_tips) as total_tips
FROM moves_chicago_taxis
WHERE trip_seconds <> 0
GROUP BY trip_end_location
ORDER BY tip_hour_rate desc;

--MonetDB

SELECT trip_end_location, round(sum(trip_tips)/(sum(trip_seconds)/60/60),2) as tip_hour_rate, sum(trip_seconds) as total_seconds, sum(trip_tips) as total_tips
FROM moves_chicago_taxis
WHERE trip_seconds <> 0
GROUP BY trip_end_location
ORDER BY tip_hour_rate desc;
