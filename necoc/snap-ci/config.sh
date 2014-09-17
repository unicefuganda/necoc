#!/bin/bash

sudo mkdir -p /data/db && sudo service mongod restart

cd ..
virtualenv necoc_env
source necoc_env/bin/activate
cd -
pip install -r requirements.txt
pip install python-coveralls
