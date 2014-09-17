from django.test import TestCase
from rest_framework.test import APITestCase


class NoSQLTestCase(TestCase):
    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass


class NoSQLAPITestCase(APITestCase):
    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass
