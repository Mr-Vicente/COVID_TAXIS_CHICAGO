
--Postgresql

CREATE UNLOGGED TABLE IF NOT EXISTS covid_chicago_taxis_n (
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
  trip_start_latitude numeric,
  trip_start_longitude numeric,
  trip_end_latitude numeric,
  trip_end_longitude numeric,
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
      REFERENCES trip_junk_dim(junk_id)
);

select count(*) as number_of_trips, date_dim.year from covid_chicago_taxis_n 
                    inner join date_dim on(covid_chicago_taxis_n.trip_end_date = date_dim.date_id) 
group by date_dim.year;

drop table covid_chicago_taxis_n;

SELECT * into covid_chicago_taxis_n FROM covid_chicago_taxis inner join date_dim on(date_dim.date_id = covid_chicago_taxis.trip_end_date)
where (year = '2019' and RANDOM() > 0.6) or
      (year = '2020' and RANDOM() > 0.6) or
      (year = '2021' and RANDOM() > 0.6);

CREATE INDEX ON covid_chicago_taxis_n(trip_id);
CREATE INDEX ON covid_chicago_taxis_n(trip_start_date);
CREATE INDEX ON covid_chicago_taxis_n(trip_start_hour);
CREATE INDEX ON covid_chicago_taxis_n(trip_end_hour);
CREATE INDEX ON covid_chicago_taxis_n(trip_end_hour);
CREATE INDEX ON covid_chicago_taxis_n(trip_junk);

SELECT * into covid_chicago_taxis_n FROM covid_chicago_taxis inner join date_dim on(date_dim.date_id = covid_chicago_taxis.trip_end_date)
where (year = '2019' and RANDOM() > 0.95) or
      (year = '2020' and RANDOM() > 0.95) or
      (year = '2021' and RANDOM() > 0.95);

SELECT * into covid_chicago_taxis_n FROM covid_chicago_taxis inner join date_dim on(date_dim.date_id = covid_chicago_taxis.trip_end_date)
where "or"("and"(year = 2019, (RAND()/2147483648) > 0.95),
      "or"("and"(year = 2020, (RAND()/2147483648) > 0.95),
      "and"(year = 2021, (RAND()/2147483648) > 0.95)));

with x as SELECT * FROM covid_chicago_taxis inner join date_dim on(date_dim.date_id = covid_chicago_taxis.trip_end_date)
where "or"("and"(year = 2019, (RAND()/2147483648) > 0.95),
      "or"("and"(year = 2020, (RAND()/2147483648) > 0.95),
      "and"(year = 2021, (RAND()/2147483648) > 0.95)))
insert into covid_chicago_taxis_n;


CREATE TABLE IF NOT EXISTS covid_chicago_taxis_n (
  trip_id text,
  taxi_id text,
  trip_seconds int,
  trip_miles float,
  trip_fare float,
  trip_tips float,
  trip_tolls float,
  trip_extras float,
  trip_total float,
  trip_start_hour text,
  trip_end_hour text,
  trip_start_date text,
  trip_end_date text,
  trip_junk text,
  trip_start_latitude float,
  trip_start_longitude float,
  trip_end_latitude float,
  trip_end_longitude float,
  PRIMARY KEY(trip_id),
  CONSTRAINT fk_start_date_n
    FOREIGN KEY(trip_start_date)
      REFERENCES date_dim(date_id),
  CONSTRAINT fk_end_date_n
    FOREIGN KEY(trip_end_date)
      REFERENCES date_dim(date_id),
  CONSTRAINT fk_start_hour_n
    FOREIGN KEY(trip_start_hour)
      REFERENCES hour_dim(hour_id),
  CONSTRAINT fk_end_hour_n
    FOREIGN KEY(trip_end_hour)
      REFERENCES hour_dim(hour_id),
  CONSTRAINT fk_trip_junk_n
    FOREIGN KEY(trip_junk)
      REFERENCES trip_junk_dim(junk_id)
);

insert into covid_chicago_taxis_n SELECT trip_id,
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
  trip_start_latitude,
  trip_start_longitude,
  trip_end_latitude,
  trip_end_longitude FROM covid_chicago_taxis inner join date_dim on date_dim.date_id = covid_chicago_taxis.trip_end_date
where RAND()/2147483648.0 > 0.95;


insert into covid_chicago_taxis_n SELECT trip_id,
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
  trip_start_latitude,
  trip_start_longitude,
  trip_end_latitude,
  trip_end_longitude FROM covid_chicago_taxis inner join date_dim on(date_dim.date_id = covid_chicago_taxis.trip_end_date)
where "or"("and"(date_dim.year = 2019, RAND()/2147483648.0 > 0.95),
      "or"("and"(date_dim.year = 2020, RAND()/2147483648.0 > 0.95),
      "and"(date_dim.year = 2021, RAND()/2147483648.0 > 0.95)));