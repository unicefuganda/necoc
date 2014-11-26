from mongoengine.django.auth import Group
from dms.models import User, Location, UserProfile
from dms.api.user_profile_endpoint import UserProfileSerializer
from dms.tests.base import MongoTestCase


class UserProfileSerializerTest(MongoTestCase):
    def setUp(self):
        self.district = Location(**dict(name='Kampala', type='district', parent=None)).save()

        self.serialized_location = dict(created_at=self.district.created_at, type=self.district.type,
                                        name=self.district.name, id=str(self.district.id))
        self.mobile_user = dict(name='timothy', phone='+256775019449', location=self.district,
                                email="timothyakampa@gmail.com")
        self.serialized_mobile_user = dict(name='timothy', phone='+256775019449', location=self.serialized_location,
                                           email="timothyakampa@gmail.com")

    def test_should_serialize_mobile_user_object(self):
        mobile_user = UserProfile(**self.mobile_user).save()
        serialized_object = UserProfileSerializer(mobile_user)
        self.assertDictContainsSubset(self.serialized_mobile_user, serialized_object.data)
        self.assertIsNotNone(serialized_object.data['id'])

    def test_should_deserialize_mobile_user_object(self):
        self.serialized_mobile_user['location'] = self.district.id
        serializer = UserProfileSerializer(data=self.serialized_mobile_user)

        self.assertTrue(serializer.is_valid())
        saved_mobile_user = serializer.save()

        self.assertTrue(isinstance(saved_mobile_user, UserProfile))
        for attribute, value in self.mobile_user.items():
            self.assertEqual(value, getattr(saved_mobile_user, attribute))

    def test_serializer_should_be_invalid_if_phone_number_is_not_unique(self):
        self.serialized_mobile_user['location'] = self.district.id
        serializer = UserProfileSerializer(data=self.serialized_mobile_user)

        self.assertTrue(serializer.is_valid())
        serializer.save()

        serializer = UserProfileSerializer(data=self.serialized_mobile_user)
        self.assertFalse(serializer.is_valid())

    def test_serializer_should_be_valid_if_model_is_being_updated(self):
        self.serialized_mobile_user['location'] = self.district.id
        serializer = UserProfileSerializer(data=self.serialized_mobile_user)

        self.assertTrue(serializer.is_valid())
        saved_profile = serializer.save()
        self.serialized_mobile_user['id'] = saved_profile.id

        serializer = UserProfileSerializer(data=self.serialized_mobile_user)
        self.assertTrue(serializer.is_valid())

    def test_serializer_should_be_invalid_if_email_is_not_unique(self):
        self.serialized_mobile_user['location'] = self.district.id
        serializer = UserProfileSerializer(data=self.serialized_mobile_user)

        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.serialized_mobile_user['phone'] = '+25632323424'
        serializer = UserProfileSerializer(data=self.serialized_mobile_user)
        self.assertFalse(serializer.is_valid())

    def test_serializer_should_be_invalid_if_username_is_not_unique(self):
        User(username='tim', password='password').save()
        self.serialized_mobile_user['location'] = self.district.id
        self.serialized_mobile_user['username'] = 'tim'
        serializer = UserProfileSerializer(data=self.serialized_mobile_user)
        self.assertFalse(serializer.is_valid())

    def test_serializer_should_be_valid_if_no_email_is_passed(self):
        self.serialized_mobile_user['location'] = self.district.id
        del self.serialized_mobile_user['email']
        serializer = UserProfileSerializer(data=self.serialized_mobile_user)
        self.assertTrue(serializer.is_valid())

    def test_empty_email_is_not_unique(self):
        self.serialized_mobile_user['location'] = self.district.id
        del self.serialized_mobile_user['email']
        serializer = UserProfileSerializer(data=self.serialized_mobile_user)
        serializer.is_valid()
        user_without_email = serializer.save()

        another_user_attr = dict(name='Haha', phone='+2567711111', location=self.district.id)

        serializer = UserProfileSerializer(data=another_user_attr)

        self.assertTrue(serializer.is_valid())

    def test_only_username_is_serialized_if_user_profile_has_a_user(self):
        mobile_user_attr = self.mobile_user.copy()
        mobile_user_attr['user'] = User(username='cage', password='haha').save()
        mobile_user = UserProfile(**mobile_user_attr).save()

        serialized_object = UserProfileSerializer(mobile_user)
        self.assertDictContainsSubset(self.serialized_mobile_user, serialized_object.data)
        self.assertEqual('cage', serialized_object.data['username'])
        self.assertFalse('user' in serialized_object.data.keys())

    def test_serializing_group_name(self):
        mobile_user_attr = self.mobile_user.copy()
        group = Group.objects().first()
        mobile_user_attr['user'] = User(username='cage', password='haha', group=group).save()
        mobile_user = UserProfile(**mobile_user_attr).save()

        serialized_object = UserProfileSerializer(mobile_user)
        self.assertEqual(group.name, serialized_object.data['group'])

    def test_serializing_group_name_when_absent(self):
        mobile_user_attr = self.mobile_user.copy()
        mobile_user = UserProfile(**mobile_user_attr).save()

        serialized_object = UserProfileSerializer(mobile_user)
        self.assertEqual('', serialized_object.data['group'])
