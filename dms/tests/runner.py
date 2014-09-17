from django.test.runner import DiscoverRunner
import mongoengine


class NoSQLTestRunner(DiscoverRunner):
    MONGODB_HOST = 'localhost'
    MONGODB_NAME = 'dms_test'
    MONGODB_DATABASE_HOST = 'mongodb://%s/%s' % (MONGODB_HOST, MONGODB_NAME)

    def __init__(self, **kwargs):
        super(NoSQLTestRunner, self).__init__(**kwargs)
        self.db = None

    def setup_databases(self):
        self.db = mongoengine.connect(self.MONGODB_NAME, host=self.MONGODB_DATABASE_HOST)

    def teardown_databases(self, *args):
        self.db.drop_database(self.MONGODB_NAME)

