from mongoengine.django.auth import User

from dms.api.password_change_endpoint import UserPasswordChangeSerializer
from dms.tests.base import MongoTestCase


class PasswordChangeSerializerTest(MongoTestCase):
    def setUp(self):
        self.user = User(username='haha')
        self.user.set_password('hehe')
        self.password_data = dict(old_password='hehe', new_password='hoho', confirm_password='hoho')

    def test_should_deserialize_user_object(self):
        serializer = UserPasswordChangeSerializer(self.user, data=self.password_data)

        self.assertTrue(serializer.is_valid())
        saved_user = serializer.save()

        self.assertTrue(isinstance(saved_user, User))
        self.assertTrue(saved_user.check_password(self.password_data['new_password']))

    def test_serializer_should_be_invalid_if_current_password_does_not_match(self):
        data = self.password_data.copy()
        data['old_password'] = 'not matched'
        serializer = UserPasswordChangeSerializer(self.user, data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(['Current password incorrect.'], serializer.errors['old_password'])

    def test_serializer_should_be_invalid_if_new_password_and_confirm_password_do_not_match(self):
        data = self.password_data.copy()
        data['confirm_password'] = 'not matched'
        serializer = UserPasswordChangeSerializer(self.user, data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(["The two password fields didn't match."], serializer.errors['confirm_password'])

    def test_new_password_is_required(self):
        data = self.password_data.copy()
        data['new_password'] = ''
        serializer = UserPasswordChangeSerializer(self.user, data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(['This field is required.'], serializer.errors['new_password'])

        del data['new_password']
        serializer = UserPasswordChangeSerializer(self.user, data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(['This field is required.'], serializer.errors['new_password'])

    def test_confirm_password_is_required(self):
        data = self.password_data.copy()
        data['confirm_password'] = ''
        serializer = UserPasswordChangeSerializer(self.user, data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(['This field is required.'], serializer.errors['confirm_password'])

        del data['confirm_password']
        serializer = UserPasswordChangeSerializer(self.user, data=data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(['This field is required.'], serializer.errors['confirm_password'])