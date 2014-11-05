from dms.models import Location
from dms.models.user import User
from dms.tests.base import MongoTestCase


class TestUserModel(MongoTestCase):

    def test_fields(self):
        user = User()
        self.assertTrue(hasattr(user, 'phone_no'))
        self.assertTrue(hasattr(user, 'location'))

    def test_save(self):
        kampala = Location(name='Kampala', type='district').save()
        user_data ={
            'username': 'cage', 'first_name':'nicolas', 'last_name':'cage', 'email':'nic@ol.as', 'password':'haha',
            'phone_no':'235669502', 'location': str(kampala.id)
        }
        User(**user_data).save()
        self.failUnless(User.objects(**user_data))