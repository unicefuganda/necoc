from mongoengine import ValidationError
from dms.models.location import Location
from dms.models.mobile_user import MobileUser
from dms.tests.base import MongoTestCase


class TestMobileUserModel(MongoTestCase):

    def setUp(self):
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()

    def tearDown(self):
        MobileUser.drop_collection()

    def test_should_create_new_user(self):
        mobile_user = dict(name='timothy', phone='+256775019449', location=self.district, email=None)
        MobileUser(**mobile_user).save()
        saved_mobile_user = MobileUser.objects(**mobile_user)
        self.assertEqual(1, saved_mobile_user.count())

    def xtest_should_not_save_a_user_without_a_phone_number_and_location(self):
        mobile_user = dict(name='timothy', email=None)
        MobileUser(**mobile_user).save()
        MobileUser.objects(**mobile_user)

        self.assertRaises(ValidationError, 'dad')
