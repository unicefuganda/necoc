from dms.models import User
from dms.models.token import Token
from dms.tests.base import MongoTestCase


class TestToken(MongoTestCase):
    def setUp(self):
        user_attrs = dict(username="navaL", first_name="NavaL", last_name="Andria", email="naval@mail.com",
                          password="xxxxxx")
        self.user = User(**user_attrs).save()

    def test_should_create_token_for_an_existing_user(self):
        Token(user=self.user).save()
        tokens = Token.objects(user=self.user)
        self.assertEqual(tokens.count(), 1)

        user_token = tokens.first()
        self.assertIsNotNone(user_token.key)
        self.assertEqual(str(user_token), user_token.key)