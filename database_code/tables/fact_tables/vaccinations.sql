--Postgresql

CREATE UNLOGGED TABLE IF NOT EXISTS vaccinations (
  vax_day_id text,
  vax_date text,
  total_doses numeric,
  fisrt_dose numeric,
  completed numeric,
  location text,
  PRIMARY KEY(vax_day_id),
  CONSTRAINT fk_date
    FOREIGN KEY(vax_date)
      REFERENCES date_dim2(date_id),
  CONSTRAINT fk_location
    FOREIGN KEY(location)
      REFERENCES location_dim(location_id)
);

COPY vaccinations(
  vax_day_id,
  vax_date,
  total_doses,
  fisrt_dose,
  completed,
  location
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/fact_tables/vaccinations.csv'
DELIMITER ','
CSV HEADER;

--MonetDB

drop table vaccinations;

CREATE TABLE IF NOT EXISTS vaccinations (
  vax_day_id text,
  vax_date text,
  total_doses INT,
  first_dose INT,
  completed INT,
  location text,
  PRIMARY KEY(vax_day_id),
    CONSTRAINT fk_date
    FOREIGN KEY(vax_date)
      REFERENCES date_dim2(date_id),
  CONSTRAINT fk_location
    FOREIGN KEY(location)
      REFERENCES location_dim(location_id)
);

COPY OFFSET 2 INTO vaccinations(
  vax_day_id,
  vax_date,
  total_doses,
  first_dose,
  completed,
  location
)
FROM '/Users/FrederioVicente/Desktop/Mestrado/5ºano/MD/projeto/tables/fact_tables/vaccinations.csv'
USING DELIMITERS ',', E'\n', '"';