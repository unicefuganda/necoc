#!/bin/bash

source ../necoc_env/bin/activate
echo $COVERALLS_REPO_TOKEN >> .coveralls.yml
coverage run manage.py test
coveralls