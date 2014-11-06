from mongoengine import ValidationError, NotUniqueError
from dms.models.location import Location
from dms.models.user_profile import UserProfile
from dms.tests.base import MongoTestCase


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
