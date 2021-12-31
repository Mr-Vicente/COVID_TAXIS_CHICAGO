
--Posgresql
DISCARD ALL;
[Restart database]
sync && sudo purge
psql [port] [DATABASE]
EXPLAIN ANALYZE
[query]


--MonetDB
mclient -u monetdb -d taxi --timer=performance

[Restart database]
sync && sudo purge
mclient -u monetdb -d [DATABASE_NAME] --timer=performance
\f trash
trace [query]