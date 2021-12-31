
--Postgresql

CREATE UNLOGGED TABLE IF NOT EXISTS date_dim (
  date_id text,
  year numeric,
  month text,
  day numeric,
  week_day text,
  is_weekend bool,
  is_holiday bool,
  covid_phase text,
  PRIMARY KEY(date_id)
);

COPY date_dim(
  date_id,
  year,
  month,
  day,
  week_day,
  is_weekend,
  is_holiday,
  covid_phase
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/dimensions/data_dimension.csv'
DELIMITER ',';

--MonetDB

drop table date_dim;

CREATE TABLE IF NOT EXISTS date_dim (
  date_id text,
  year_ INT,
  month_ TEXT,
  day_ INT,
  week_day text,
  is_weekend bool,
  is_holiday bool,
  covid_phase text,
  PRIMARY KEY(date_id)
);

COPY into date_dim(
  date_id,
  year_,
  month_,
  day_,
  week_day,
  is_weekend,
  is_holiday,
  covid_phase
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/dimensions/data_dimension.csv'
USING DELIMITERS ',', E'\n', '"';