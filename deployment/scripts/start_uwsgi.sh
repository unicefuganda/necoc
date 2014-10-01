#!/bin/bash
sleep 5;
/necoc/deployment/scripts/load_fixtures.sh
sleep 1; /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/necoc-uwsgi.ini
