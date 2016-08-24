import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMIN_EMAIL = 'ayo@yo.yo'

MONGODB_USER = ''
MONGODB_PASSWORD = ''
MONGODB_HOST = 'localhost'
MONGODB_NAME = 'dms'
MONGODB_DATABASE_HOST = 'mongodb://%s/%s' % (MONGODB_HOST, MONGODB_NAME)
DISTRICT_GROUPS = ['DDMC', 'CAO', 'DDMC Chairperson']


if 'test' in sys.argv:
    REST_FRAMEWORK = {}

if ('test' in sys.argv) or ('0.0.0.0:7999' in sys.argv) or ('test_user' in sys.argv):
    TEST_RUNNER = 'dms.tests.runner.NoSQLTestRunner'

    MESSAGE_LOCATION_INDEX = 2
    POLL_RESPONSE_KEYWORD_INDEX = 2
    MESSAGE_SEPARATOR = '.'

    MONGODB_HOST = 'localhost'
    MONGODB_NAME = 'dms_test'
    MONGODB_DATABASE_HOST = 'mongodb://%s/%s' % (MONGODB_HOST, MONGODB_NAME)

    API_TOKEN = 'ayoyoyoooooooo'
    API_URL = 'http://localhost:7999/api/v1/mobile-users'
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    HOSTNAME = 'http://localhost:8000' #No trailing slash
    API_USER_PASS = '10123456'
    API_AUTHORIZATION_STEP = '123445'

from mongoengine.connection import connect
connect(MONGODB_NAME, host=MONGODB_DATABASE_HOST)

