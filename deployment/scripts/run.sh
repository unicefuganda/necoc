#!/bin/bash
mkdir -p /data/db
sed -i "s/##SERVER_NAME##/$NGINX_SERVER_NAME/g" /etc/nginx/conf.d/necoc.conf && service supervisor start
