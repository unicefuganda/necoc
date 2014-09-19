#!/bin/bash

source ../necoc_env/bin/activate
coverage run manage.py test
coveralls