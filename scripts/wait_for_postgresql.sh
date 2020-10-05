#!/bin/bash

for i in $(seq 1 10); do
  echo "-- pinging PostgreSQL server: attempt $i ..."
  nc -z localhost 5432 && echo Success && exit 0
  sleep 1
done

echo Failed waiting for Postgres && exit 1
