
--postgresql

CREATE UNLOGGED TABLE IF NOT EXISTS facilities (
  facility_id text,
  name text,
  facility_type text,
  longitude numeric,
  latitude numeric,
  zip_code numeric,
  zip_area numeric,
  PRIMARY KEY(facility_id)
);

COPY facilities(
  facility_id,
  name,
  facility_type,
  longitude,
  latitude,
  zip_code,
  zip_area
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/fact_tables/facilities.csv'
DELIMITER ','
CSV;

--MonetDB

drop table facilities;

CREATE TABLE IF NOT EXISTS facilities (
  facility_id text,
  name text,
  facility_type text,
  longitude FLOAT,
  latitude FLOAT,
  zip_code FLOAT,
  zip_area FLOAT,
  PRIMARY KEY(facility_id)
);

COPY into facilities(
  facility_id,
  name,
  facility_type,
  longitude,
  latitude,
  zip_code,
  zip_area
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/fact_tables/facilities.csv'
USING DELIMITERS ',', E'\n', '"';


