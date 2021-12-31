
--Postgresql

CREATE UNLOGGED TABLE IF NOT EXISTS trip_junk_dim (
  junk_id text,
  payment_type text,
  company text,
  PRIMARY KEY(junk_id)
);

COPY trip_junk_dim(
  junk_id,
  payment_type,
  company
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/dimensions/trip_junk_dimension.csv'
DELIMITER ','
CSV;

--MonetDB

drop table trip_junk_dim;

CREATE TABLE IF NOT EXISTS trip_junk_dim (
  junk_id text,
  payment_type text,
  company text,
  PRIMARY KEY(junk_id)
);

COPY into trip_junk_dim(
  junk_id,
  payment_type,
  company
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/dimensions/trip_junk_dimension.csv'
USING DELIMITERS ',', E'\n', '"';