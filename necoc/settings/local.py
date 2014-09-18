import sys
import mongoengine

DEBUG = True
TEMPLATE_DEBUG = DEBUG

if ('test' in sys.argv) or ('harvest' in sys.argv):
    TEST_RUNNER = 'dms.tests.runner.NoSQLTestRunner'

    print 'haha'
    MONGODB_HOST = 'localhost'
    MONGODB_NAME = 'dms_test'
    MONGODB_DATABASE_HOST = 'mongodb://%s/%s' % (MONGODB_HOST, MONGODB_NAME)

    from mongoengine.connection import connect, disconnect
    disconnect()
    connect(MONGODB_NAME, host=MONGODB_DATABASE_HOST)
