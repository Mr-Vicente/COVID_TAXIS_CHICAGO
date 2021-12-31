
--Postgresql

CREATE EXTENSION postgis;

CREATE UNLOGGED TABLE IF NOT EXISTS moves_chicago_taxis (
  trip_id text,
  taxi_id text,
  trip_seconds numeric,
  trip_miles numeric,
  trip_fare numeric,
  trip_tips numeric,
  trip_tolls numeric,
  trip_extras numeric,
  trip_total numeric,
  trip_start_hour text,
  trip_end_hour text,
  trip_start_date text,
  trip_end_date text,
  trip_junk text,
  trip_start_location text,
  trip_end_location text,
  PRIMARY KEY(trip_id),
  CONSTRAINT fk_start_date
    FOREIGN KEY(trip_start_date)
      REFERENCES date_dim(date_id),
  CONSTRAINT fk_end_date
    FOREIGN KEY(trip_end_date)
      REFERENCES date_dim(date_id),
  CONSTRAINT fk_start_hour
    FOREIGN KEY(trip_start_hour)
      REFERENCES hour_dim(hour_id),
  CONSTRAINT fk_end_hour
    FOREIGN KEY(trip_end_hour)
      REFERENCES hour_dim(hour_id),
  CONSTRAINT fk_trip_junk
    FOREIGN KEY(trip_junk)
      REFERENCES trip_junk_dim(junk_id),
  CONSTRAINT fk_start_location
    FOREIGN KEY(trip_start_location)
      REFERENCES location_grid_dim(location_id),
  CONSTRAINT fk_end_location
    FOREIGN KEY(trip_end_location)
      REFERENCES location_grid_dim(location_id)
);

COPY moves_chicago_taxis(
  trip_id,
  taxi_id,
  trip_seconds,
  trip_miles,
  trip_fare,
  trip_tips,
  trip_tolls,
  trip_extras,
  trip_total,
  trip_start_hour,
  trip_end_hour,
  trip_start_date,
  trip_end_date,
  trip_junk,
  trip_start_location,
  trip_end_location 
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/fact_tables/moves_chicago_taxis.csv'
DELIMITER ','
CSV HEADER;

--MonetDB

drop table moves_chicago_taxis;

CREATE TABLE IF NOT EXISTS moves_chicago_taxis (
  trip_id text,
  taxi_id text,
  trip_seconds numeric,
  trip_miles numeric,
  trip_fare numeric,
  trip_tips numeric,
  trip_tolls numeric,
  trip_extras numeric,
  trip_total numeric,
  trip_start_hour text,
  trip_end_hour text,
  trip_start_date text,
  trip_end_date text,
  trip_junk text,
  trip_start_location text,
  trip_end_location text,
  PRIMARY KEY(trip_id),
  CONSTRAINT fk_start_date_move
    FOREIGN KEY(trip_start_date)
      REFERENCES date_dim(date_id),
  CONSTRAINT fk_end_date_move
    FOREIGN KEY(trip_end_date)
      REFERENCES date_dim(date_id),
  CONSTRAINT fk_start_hour_move
    FOREIGN KEY(trip_start_hour)
      REFERENCES hour_dim(hour_id),
  CONSTRAINT fk_end_hour_move
    FOREIGN KEY(trip_end_hour)
      REFERENCES hour_dim(hour_id),
  CONSTRAINT fk_trip_junk_move
    FOREIGN KEY(trip_junk)
      REFERENCES trip_junk_dim(junk_id),
  CONSTRAINT fk_start_location_move
    FOREIGN KEY(trip_start_location)
      REFERENCES location_grid_dim(location_id),
  CONSTRAINT fk_end_location_move
    FOREIGN KEY(trip_end_location)
      REFERENCES location_grid_dim(location_id)
);

COPY OFFSET 2 into moves_chicago_taxis(
  trip_id,
  taxi_id,
  trip_seconds,
  trip_miles,
  trip_fare,
  trip_tips,
  trip_tolls,
  trip_extras,
  trip_total,
  trip_start_hour,
  trip_end_hour,
  trip_start_date,
  trip_end_date,
  trip_junk,
  trip_start_location,
  trip_end_location 
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/fact_tables/moves_chicago_taxis.csv'
USING DELIMITERS ',', E'\n', '"';