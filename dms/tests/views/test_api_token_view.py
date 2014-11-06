import ast
from django.test import Client
from dms.models import User
from dms.tests.base import MongoAPITestCase


class ObtainAPITokenViewTest(MongoAPITestCase):
    def setUp(self):
        self.client = Client()

    def test_post_export_poll_response(self):
        user = User.objects.create(username='api_user', email='api_user@email.email')
        user.set_password('password')
        user.save()
        user_data = dict(username='api_user', password='password')
        response = self.client.post('/api-token-auth/', user_data)
        self.assertEquals(200, response.status_code)

        formatted_response = ast.literal_eval(response.content)
        self.assertIsNotNone(formatted_response['token'])
