from rest_framework.test import APITestCase
from django.test import TestCase


class MongoTestCase(TestCase):
    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass


class NoSQLAPITestCase(APITestCase):
    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass
