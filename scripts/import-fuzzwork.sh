#!/usr/bin/env bash

#wget https://www.fuzzwork.co.uk/dump/postgres-latest.dmp.bz2 -O sde-workspace/postgres-latest.dmp.bz2
#
#bunzip2 -d sde-workspace/postgres-latest.dmp.bz2

pg_restore -d evebot -v -O -x --disable-triggers -h 127.0.0.1 -p 5432 -U evebot -W sde-workspace/postgres-latest.dmp
