#!/bin/bash
if [  "$LOAD_DATA" == "True" ]; then
    sleep 10;
    cd /necoc/dms/fixtures && python /necoc/manage.py import_location uganda_location_from_devtrac2.csv;
    python /necoc/manage.py create_user_groups;
    python /necoc/manage.py create_super_user;
    exit 0;
fi