from mongoengine import ValidationError, NotUniqueError
from dms.models import User, Location, UserProfile
from dms.tests.base import MongoTestCase
from necoc import settings


class TestUserProfileModel(MongoTestCase):
    def setUp(self):
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()

    def tearDown(self):
        UserProfile.drop_collection()

    def test_should_create_new_user(self):
        mobile_user = dict(name='timothy', phone='+256775019449', location=self.district, email=None)
        UserProfile(**mobile_user).save()
        saved_mobile_user = UserProfile.objects(**mobile_user)
        self.assertEqual(1, saved_mobile_user.count())

    def test_should_not_save_a_user_without_a_phone_number_and_location(self):
        mobile_user = dict(name='timothy', email=None)
        self.assertRaises(ValidationError, UserProfile(**mobile_user).save)

    def test_should_not_save_a_users_with_the_same_phone_number(self):
        mobile_user_one = dict(name='timothy', phone='+256775019449', location=self.district, email=None)
        mobile_user_two = dict(name='James', phone='+256775019449', location=self.district, email=None)

        UserProfile(**mobile_user_one).save()
        self.assertRaises(NotUniqueError, UserProfile(**mobile_user_two).save)

    def test_saving_a_system_user(self):
        user = User(username='haha', password='hehe').save()
        user_profile_attr = dict(name='timothy', phone='+256775019449', location=self.district, email=None, user=user)

        UserProfile(**user_profile_attr).save()

        self.assertEqual(user, UserProfile.objects.get(**user_profile_attr).user)

    def test_get_username(self):
        user = User(username='haha', password='hehe').save()
        user_profile_attr = dict(name='timothy', phone='+256775019449', location=self.district, email=None, user=user)
        profile = UserProfile(**user_profile_attr).save()

        self.assertEqual('haha', profile.username())

    def test_get_user_id(self):
        user = User(username='haha', password='hehe').save()
        user_profile_attr = dict(name='timothy', phone='+256775019449', location=self.district, email=None, user=user)
        profile = UserProfile(**user_profile_attr).save()

        self.assertEqual(str(user.id), profile.user_id())

    def test_get_username_from_regular_user(self):
        user_profile_attr = dict(name='timothy', phone='+256775019449', location=self.district, email=None)
        profile = UserProfile(**user_profile_attr).save()

        self.assertEqual('', profile.username())

    def test_should_save_photo_of_user(self):
        user_profile_attr = dict(name='timothy', phone='+256775019449', location=self.district, email=None)
        profile = UserProfile(**user_profile_attr)
        user_photo = open(settings.PROJECT_ROOT + '/../dms/tests/test.jpg', 'rb')
        profile.photo.put(user_photo, content_type='image/content_type')
        profile.save()
        reloaded_profile = UserProfile.objects(id=profile.id).first()
        self.assertEqual(reloaded_profile.photo.read(),
                         open(settings.PROJECT_ROOT + '/../dms/tests/test.jpg', 'rb').read())
        self.assertEqual(reloaded_profile.photo.content_type, 'image/content_type')
        self.assertEqual(reloaded_profile.photo_uri(), '/api/v1/photo/' + str(reloaded_profile.id))