import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

if ('test' in sys.argv) or ('0.0.0.0:7999' in sys.argv):
    TEST_RUNNER = 'dms.tests.runner.NoSQLTestRunner'

    MONGODB_HOST = 'localhost'
    MONGODB_NAME = 'dms_test'
    MONGODB_DATABASE_HOST = 'mongodb://%s/%s' % (MONGODB_HOST, MONGODB_NAME)

    from mongoengine.connection import connect, disconnect, get_connection
    disconnect()
    connect(MONGODB_NAME, host=MONGODB_DATABASE_HOST)
    connection = get_connection()
    connection.drop_database(MONGODB_NAME)

    API_TOKEN = 'ayoyoyoooooooo'
    # API_URL = 'http://domaindoesnotexist.commmm'
    API_URL = 'http://localhost:7999/api/v1/mobile-users'

