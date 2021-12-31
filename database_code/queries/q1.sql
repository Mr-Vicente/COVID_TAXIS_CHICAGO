-- Tables used: taxis, vaccination locations, hospitals, clinics, testing locations.
-- radius: 10km
-- ST_MakePoint(start_location_lon,end_location_lat) if no points available

--Postgresql
SELECT COUNT(*), hour, facility_type FROM (
    SELECT hour, facility_type, name FROM covid_chicago_taxis_n JOIN facilities
    ON ST_DistanceSphere(
        ST_MakePoint(trip_end_longitude,trip_end_latitude),
        ST_MakePoint(facilities.longitude,facilities.latitude) 
        ) <= 10
    inner JOIN date_dim on (date_dim.date_id = covid_chicago_taxis_n.trip_end_date)
    inner JOIN hour_dim on (hour_dim.hour_id = covid_chicago_taxis_n.trip_end_hour)
    WHERE (date_dim.covid_phase <> 'pre-covid' and (facilities.facility_type = 'hospital'  or 
                            facilities.facility_type = 'clinic'    or
                            facilities.facility_type = 'test_site'))
          or (date_dim.year = '2021' and facilities.facility_type = 'vax_site')
)as x
GROUP BY hour, facility_type;


--MonetDB
SELECT COUNT(*), hour_, facility_type FROM (
select hour_, facility_type FROM covid_chicago_taxis_n inner JOIN facilities
    ON ST_Distance(
        ST_MakePoint(trip_end_longitude,trip_end_latitude),
        ST_MakePoint(facilities.longitude,facilities.latitude) 
        ) <= 10
    inner JOIN date_dim on date_dim.date_id = covid_chicago_taxis_n.trip_end_date
    inner JOIN hour_dim on hour_dim.hour_id = covid_chicago_taxis_n.trip_end_hour
    WHERE "or"("and"(date_dim.covid_phase <> 'pre-covid', "or"(facilities.facility_type = 'hospital', "or"( 
                            facilities.facility_type = 'clinic', 
                            facilities.facility_type = 'test_site'))),
               "and"(date_dim.year_ >= 2021, facility_type = 'vax_site'))
    )as x
GROUP BY hour_, facility_type;