#!/bin/bash
if [  "$LOAD_DATA" == "True" ]; then
    sleep 10;
    cd /necoc/dms/fixtures && python manage.py import_location uganda_location.csv;
    exit 0;
fi