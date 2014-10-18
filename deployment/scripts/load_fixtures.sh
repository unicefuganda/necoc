#!/bin/bash
if [  "$LOAD_DATA" == "yes" ]; then
    sleep 10;
    mongoimport --db dms --collection location --type csv --headerline --file /necoc/dms/fixtures/districts.csv;
    exit 0;
fi