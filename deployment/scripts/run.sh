#!/bin/bash
sed -i "s/##API_TOKEN##/$API_TOKEN/g" /etc/uwsgi/apps-enabled/necoc-uwsgi.ini
sed -i "s/##SERVER_NAME##/$NGINX_SERVER_NAME/g" /etc/nginx/conf.d/necoc.conf && service supervisor start
