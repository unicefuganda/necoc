from django.test import Client
from dms.tests.base import MongoTestCase


class TestHome(MongoTestCase):

    def setUp(self):
        self.homepage_url = '/'
        self.client = Client()

    def test_should_get_homepage(self):
        response = self.client.get(self.homepage_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')
