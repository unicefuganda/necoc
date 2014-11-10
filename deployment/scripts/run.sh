#!/bin/bash
sed -i "s/##API_TOKEN##/$API_TOKEN/g" /etc/uwsgi/apps-enabled/necoc-uwsgi.ini
sed -i "s/##API_TOKEN##/$API_TOKEN/g" /etc/supervisor/conf.d/supervisor.conf
sed -i "s/##LOAD_DATA##/$LOAD_DATA/g" /etc/supervisor/conf.d/supervisor.conf
sed -i "s/##EMAIL_PASSWORD##/$EMAIL_PASSWORD/g" /etc/uwsgi/apps-enabled/necoc-uwsgi.ini
sed -i "s/##EMAIL_PASSWORD##/$EMAIL_PASSWORD/g" /etc/supervisor/conf.d/supervisor.conf
sed -i "s/##SERVER_NAME##/$NGINX_SERVER_NAME/g" /etc/nginx/conf.d/necoc.conf && service supervisor start
