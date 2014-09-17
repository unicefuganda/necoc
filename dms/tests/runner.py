from django.test.runner import DiscoverRunner


class NoSQLTestRunner(DiscoverRunner):
    MONGODB_HOST = 'localhost'
    MONGODB_NAME = 'dms_test'
    MONGODB_DATABASE_HOST = 'mongodb://%s/%s' % (MONGODB_HOST, MONGODB_NAME)

    def setup_databases(self, **kwargs):
        from mongoengine.connection import connect, disconnect
        disconnect()
        connect(self.MONGODB_NAME, host=self.MONGODB_DATABASE_HOST)
        return super(NoSQLTestRunner, self).setup_databases(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        from mongoengine.connection import get_connection, disconnect
        connection = get_connection()
        connection.drop_database(self.MONGODB_NAME)
        disconnect()
        return super(NoSQLTestRunner, self).teardown_databases(old_config, **kwargs)

