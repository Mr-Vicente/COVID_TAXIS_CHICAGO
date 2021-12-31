
CREATE UNLOGGED TABLE IF NOT EXISTS chicago_taxis_grid (
  id SERIAL,
  most_popular_taxi_id text,
  amount_of_trips numeric,
  avg_trip_seconds numeric,
  avg_trip_miles numeric,
  avg_fare numeric,
  avg_tips numeric,
  avg_tolls numeric,
  avg_extras numeric,
  avg_trip_total numeric,
  most_popular_payment_type text,
  most_popular_company text,
  pickup_centroid_location numeric,
  dropoff_centroid_location numeric
);

SELECT taxi_id as most_popular_taxi_id, n_trips, avg_trip_seconds, avg_trip_miles, avg_fare, avg_tips, avg_tolls, avg_extras, avg_trip_total, payment_type as most_popular_payment_type, company as most_popular_company, pickup_centroid_location, dropoff_centroid_location
INTO chicago_taxis_grid 
from (
    (SELECT row_number() OVER (ORDER BY trip_location_start, trip_location_end) as r, taxi_id from ((SELECT COUNT(*) AS taxi_id_trips, taxi_id, trip_location_start, trip_location_end FROM chicago_taxis GROUP BY taxi_id, trip_location_start, trip_location_end) as x inner join
    (SELECT MAX(taxi_id_trips) as m, trip_location_start as p_lo, trip_location_end as p_la FROM (SELECT COUNT(*) AS taxi_id_trips, taxi_id, trip_location_start, trip_location_end FROM chicago_taxis GROUP BY taxi_id, trip_location_start, trip_location_end) AS most_popular_taxi_id group by trip_location_start, trip_location_end) as y
    on x.taxi_id_trips = y.m and x.trip_location_start = y.p_lo and x.trip_location_end = y.p_la) AS most_popular_taxi_id) as a
    natural join 
    (SELECT row_number() OVER (ORDER BY trip_location_start, trip_location_end) as r, AVG(trip_seconds), AVG(trip_miles), AVG(fare),
            COUNT(*) as n_trips ,AVG(trip_seconds) as avg_trip_seconds, AVG(trip_miles) as avg_trip_miles,
            AVG(fare) as avg_fare, AVG(tips) as avg_tips, 
            AVG(tolls) as avg_tolls, AVG(extras) as avg_extras, AVG(trip_total) as avg_trip_total,
            trip_location_start as pickup_centroid_location, trip_location_end as dropoff_centroid_location
    FROM chicago_taxis 
    GROUP BY trip_location_start, trip_location_end) as b
    natural join 
    (SELECT row_number() OVER (ORDER BY trip_location_start, trip_location_end) as r, payment_type from ((SELECT COUNT(*) AS payment_type_trips, payment_type, trip_location_start, trip_location_end FROM chicago_taxis GROUP BY payment_type, trip_location_start, trip_location_end) as x inner join
    (SELECT MAX(payment_type_trips) as m, trip_location_start as p_lo, trip_location_end as p_la FROM (SELECT COUNT(*) AS payment_type_trips, payment_type, trip_location_start, trip_location_end FROM chicago_taxis GROUP BY payment_type, trip_location_start, trip_location_end) AS most_popular_payment_type group by trip_location_start, trip_location_end) as y
    on x.payment_type_trips = y.m and x.trip_location_start = y.p_lo and x.trip_location_end = y.p_la) AS most_popular_payment_type) as c
    natural join 
    (SELECT row_number() OVER (ORDER BY trip_location_start, trip_location_end desc) as r, company from ((SELECT COUNT(*) AS company_trips, company, trip_location_start, trip_location_end FROM chicago_taxis GROUP BY company, trip_location_start, trip_location_end) as x inner join
    (SELECT MAX(company_trips) as m, trip_location_start as p_lo, trip_location_end as p_la FROM (SELECT COUNT(*) AS company_trips, company, trip_location_start, trip_location_end FROM chicago_taxis GROUP BY company, trip_location_start, trip_location_end) AS most_popular_company group by trip_location_start, trip_location_end) as y
    on x.company_trips = y.m and x.trip_location_start = y.p_lo and x.trip_location_end = y.p_la) AS most_popular_company) as d
);