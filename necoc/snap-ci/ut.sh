#!/bin/bash
pip install python-coveralls
coverage run manage.py test
coveralls