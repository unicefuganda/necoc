NECOC DMS APPLICATION
=====================

Coding Standards
----------------
1.  Tabs should be 4 spaces, using spaces rather than tab character

2.  Method names and variables should be lower case with underscores eg def method_name:

SETTING UP NECOC ON YOUR MACHINE
-----------------------------------
* Install Python
* Install MongoDB
* Add API_TOKEN environment variable (for the development variable, any string can work.)
* mongodb should be running and after cloning the repo (see below), adjust db settings in settings/base.py or settings/local.py

##Git

        git clone https://github.com/unicefuganda/necoc.git

        cd necoc

        virtualenv .necoc --no-site-packages

        source .necoc/bin/activate

        pip install -r requirements.txt

        python manage.py runserver

==
TESTS
------
* Unit and integration test are run:
        python manage.py test

* functional and end-to-end as well as js unit tests are run
        bla bla

Done!! you're good to go :)

Filenaming convention:
* for tests: test_[[OBJECT]]_[[ACTION]].py
e.g: test_disaster_form.py, test_disaster_views.py,...

====

[![Build Status](https://snap-ci.com/unicefuganda/necoc/branch/master/build_image)](https://snap-ci.com/unicefuganda/necoc/branch/master)
[![Coverage Status](https://coveralls.io/repos/unicefuganda/necoc/badge.png?branch=master)](https://coveralls.io/r/unicefuganda/necoc?branch=master)
