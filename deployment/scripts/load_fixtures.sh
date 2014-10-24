#!/bin/bash
if [  "$LOAD_DATA" == "True" ]; then
    sleep 10;
    cd /necoc/dms/fixtures && python /necoc/manage.py import_location uganda_location_unique.csv;
    exit 0;
fi