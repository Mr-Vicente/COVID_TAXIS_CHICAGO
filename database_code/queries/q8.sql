--Postgresql

SELECT trip_id,  year, month, day ,facility_type, name as facility_name, trip_end_latitude, trip_end_longitude, f.latitude as facility_latitude, f.longitude as facility_longitude
from covid_chicago_taxis as c_t inner join facilities as f
on (ST_DistanceSphere(
        ST_MakePoint(trip_end_longitude,trip_end_latitude), 
        ST_MakePoint(longitude,latitude)) <= 10)
inner join date_dim as d on (c_t.trip_end_date = d.date_id)
WHERE (covid_phase <> 'pre-covid' and (facility_type = 'hospital'  or 
                                        facility_type = 'clinic'    or
                                        facility_type = 'test_site'))
        or (year= 2021 and facility_type = 'vax_site')

limit 100;

--MonetDB

SELECT trip_id,  year_, month_, day_ ,facility_type, name as facility_name, trip_end_latitude, trip_end_longitude, f.latitude as facility_latitude, f.longitude as facility_longitude
FROM covid_chicago_taxis as c_t inner join facilities as f
on (ST_Distance(
        ST_MakePoint(trip_end_longitude,trip_end_latitude), 
        ST_MakePoint(longitude,latitude)) <= 10)
INNER JOIN date_dim AS d on (c_t.trip_end_date = d.date_id)
WHERE "or"("and"(d.covid_phase <> 'pre-covid', "or"(f.facility_type = 'hospital', "or"( 
                            f.facility_type = 'clinic', 
                            f.facility_type = 'test_site'))),
               "and"(d.year_ >= 2021, f.facility_type = 'vax_site'))

limit 100;