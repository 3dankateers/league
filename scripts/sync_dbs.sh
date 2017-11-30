ssh tor@108.168.124.43 "PGPASSWORD=Postgres1423 pg_dump -h localhost -U postgres -d league" | PGPASSWORD=Postgres1423 psql -h localhost -U postgres -d league
