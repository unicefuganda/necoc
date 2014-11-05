from dms.api.location_endpoint import LocationSerializer
from dms.api.user_endpoint import UserSerializer
from dms.models.location import Location
from dms.models.user import User
from dms.tests.base import MongoTestCase


class UserSerializerTest(MongoTestCase):
    def setUp(self):
        self.kampala = Location(name='Kampala', type='district').save()
        self.user_data = {
            'username': 'cage', 'first_name': 'nicolas', 'last_name': 'cage', 'email': 'nic@ol.as', 'password': 'haha',
            'phone_no': '235669502', 'location': str(self.kampala.id)
        }

    def test_should_serialize_user_object(self):
        user = User(**self.user_data).save()
        serialized_object = UserSerializer(user)

        expected_data = self.user_data.copy()
        del expected_data['password']
        del expected_data['location']

        self.assertDictContainsSubset(expected_data, serialized_object.data)