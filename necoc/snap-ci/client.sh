#!/bin/sh
cd ../../dms/client/app && bower install
cd ../../dms/client && npm install
sudo npm install -g grunt-cli