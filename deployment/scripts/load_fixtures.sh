#!/bin/bash
if [  "$LOAD_DATA" == 1 ]; then
    sleep 10;
    mongoimport --db dms --collection location --type csv --headerline --file /necoc/dms/fixtures/districts.csv;
    exit 0;
fi