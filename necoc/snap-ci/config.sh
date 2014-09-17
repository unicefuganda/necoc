#!/bin/bash

sudo mkdir -p /data/db && sudo service mongod restart
pip install -r requirements.txt
