
--Postgresql

CREATE UNLOGGED TABLE IF NOT EXISTS location_grid_dim (
  location_id text,
  longitude numeric,
  latitude numeric,
  zip_code numeric,
  zip_area numeric,
  PRIMARY KEY(location_id)
);

COPY location_grid_dim(
  location_id,
  longitude,
  latitude,
  zip_code,
  zip_area
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/dimensions/location_grid_dimension.csv'
DELIMITER ','
CSV;

--MonetDB

drop table location_grid_dim;

CREATE TABLE IF NOT EXISTS location_grid_dim (
  location_id text,
  longitude float,
  latitude float,
  zip_code int,
  zip_area int,
  PRIMARY KEY(location_id)
);

COPY into location_grid_dim(
  location_id,
  longitude,
  latitude,
  zip_code,
  zip_area
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/dimensions/location_grid_dimension.csv'
USING DELIMITERS ',', E'\n', '"';