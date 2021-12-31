
--Postgresql

SELECT payment_type, covid_phase, SUM(trip_tips) as total_exchange, TRUNC(SUM(trip_tips)/COUNT(trip_tips),2) as ratio from covid_chicago_taxis 
inner join date_dim
on(date_dim.date_id = covid_chicago_taxis.trip_end_date)
inner join trip_junk_dim
on(trip_junk_dim.junk_id = covid_chicago_taxis.trip_junk)
GROUP BY covid_phase, payment_type
order by ratio desc, total_exchange desc;

--MonetDB

SELECT payment_type, covid_phase, SUM(trip_tips) as total_exchange, round(SUM(trip_tips)/COUNT(trip_tips),2) as ratio from covid_chicago_taxis 
inner join date_dim
on(date_dim.date_id = covid_chicago_taxis.trip_end_date)
inner join trip_junk_dim
on(trip_junk_dim.junk_id = covid_chicago_taxis.trip_junk)
GROUP BY covid_phase, payment_type
order by ratio desc, total_exchange desc;