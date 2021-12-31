
--Postgresql
SELECT * FROM pg_catalog.pg_tables
where tableowner = 'FrederioVicente';

drop table covid_chicago_taxis;
drop table moves_chicago_taxis;
drop table covid_chicago_taxis_n;
drop table chicago_taxis_grid_time;
drop table location_grid_dim;

--MonetDB
select tables.name from tables where tables.system=false ;