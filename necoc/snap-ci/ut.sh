#!/bin/bash

echo $COVERALLS_REPO_TOKEN >> .coveralls.yml
coverage run manage.py test
coveralls