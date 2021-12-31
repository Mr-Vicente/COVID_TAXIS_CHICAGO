
--Postgresql

CREATE UNLOGGED TABLE IF NOT EXISTS hour_dim (
  hour_id text,
  hour numeric,
  minute numeric,
  is_busy_hour bool,
  PRIMARY KEY(hour_id)
);

COPY hour_dim(
  hour_id,
  hour,
  minute,
  is_busy_hour
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/dimensions/hour_dimension.csv'
DELIMITER ',';

--MonetDB

drop table hour_dim;

CREATE TABLE IF NOT EXISTS hour_dim (
  hour_id text,
  hour_ INT,
  minute_ INT,
  is_busy_hour bool,
  PRIMARY KEY(hour_id)
);

COPY into hour_dim(
  hour_id,
  hour_,
  minute_,
  is_busy_hour
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/dimensions/hour_dimension.csv'
USING DELIMITERS ',', E'\n', '"';