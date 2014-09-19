#!/bin/bash

source ../necoc_env/bin/activate

cd ../../dms/client/app && bower install
cd ../../dms/client && npm install
sudo npm install -g grunt-cli