
CREATE UNLOGGED TABLE IF NOT EXISTS chicago_taxis_grid_time (
  id SERIAL,
  dropoff_date text,
  dropoff_hour text,
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
  dropoff_centroid_location text,
    PRIMARY KEY(id),
  CONSTRAINT fk_end_date
    FOREIGN KEY(dropoff_date)
      REFERENCES date_dim(date_id),
  CONSTRAINT fk_end_hour
    FOREIGN KEY(dropoff_hour)
      REFERENCES hour_dim(hour_id),
  CONSTRAINT fk_end_location
    FOREIGN KEY(dropoff_centroid_location)
      REFERENCES location_grid_dim(location_id)
);

SELECT taxi_id as most_popular_taxi_id, n_trips, avg_trip_seconds, avg_trip_miles, avg_fare, avg_tips, avg_tolls, avg_extras, avg_trip_total, payment_type as most_popular_payment_type, company as most_popular_company, dropoff_centroid_location
INTO chicago_taxis_grid_time 
from (
    (SELECT row_number() OVER (ORDER BY  trip_end_location) as r, taxi_id from ((SELECT COUNT(*) AS taxi_id_trips, taxi_id,  trip_end_location FROM moves_chicago_taxis GROUP BY taxi_id,  trip_end_location) as x inner join
    (SELECT MAX(taxi_id_trips) as m,  trip_end_location as p_la FROM (SELECT COUNT(*) AS taxi_id_trips, taxi_id,  trip_end_location FROM moves_chicago_taxis GROUP BY taxi_id,  trip_end_location) AS most_popular_taxi_id group by  trip_end_location) as y
    on x.taxi_id_trips = y.m  and x.trip_end_location = y.p_la) AS m_p_taxi) as a
    natural join 
    (SELECT row_number() OVER (ORDER BY  trip_end_location) as r, AVG(trip_seconds), AVG(trip_miles),
            COUNT(*) as n_trips ,AVG(trip_seconds) as avg_trip_seconds, AVG(trip_miles) as avg_trip_miles,
            AVG(trip_fare) as avg_fare, AVG(trip_tips) as avg_tips, 
            AVG(trip_tolls) as avg_tolls, AVG(trip_extras) as avg_extras, AVG(trip_total) as avg_trip_total,
            trip_end_location as dropoff_centroid_location
    FROM moves_chicago_taxis 
    GROUP BY  trip_end_location, ) as b
    natural join 
    (SELECT row_number() OVER (ORDER BY  trip_end_location) as r, payment_type from ((SELECT COUNT(*) AS payment_type_trips, payment_type,  trip_end_location FROM moves_chicago_taxis inner join trip_junk_dim on (moves_chicago_taxis.trip_junk = trip_junk_dim.junk_id) GROUP BY payment_type,  trip_end_location) as x inner join
    (SELECT MAX(payment_type_trips) as m,  trip_end_location as p_la FROM (SELECT COUNT(*) AS payment_type_trips, payment_type,  trip_end_location FROM moves_chicago_taxis inner join trip_junk_dim on (moves_chicago_taxis.trip_junk = trip_junk_dim.junk_id) GROUP BY payment_type,  trip_end_location) AS most_popular_payment_type group by  trip_end_location) as y
    on x.payment_type_trips = y.m  and x.trip_end_location = y.p_la) AS m_p_payment_type) as c
    natural join 
    (SELECT row_number() OVER (ORDER BY  trip_end_location desc) as r, company from ((SELECT COUNT(*) AS company_trips, company,  trip_end_location FROM moves_chicago_taxis inner join trip_junk_dim on (moves_chicago_taxis.trip_junk = trip_junk_dim.junk_id) GROUP BY company,  trip_end_location) as x inner join
    (SELECT MAX(company_trips) as m,  trip_end_location as p_la FROM (SELECT COUNT(*) AS company_trips, company,  trip_end_location FROM moves_chicago_taxis inner join trip_junk_dim on (moves_chicago_taxis.trip_junk = trip_junk_dim.junk_id) GROUP BY company,  trip_end_location) AS most_popular_company group by  trip_end_location) as y
    on x.company_trips = y.m  and x.trip_end_location = y.p_la) AS m_p_company) as d
);