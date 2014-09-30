#!/bin/bash
mongoimport --db dms --collection location --type csv --headerline --file dms/fixtures/districts.csv