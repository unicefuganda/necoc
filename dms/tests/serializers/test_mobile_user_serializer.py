from dms.api.mobile_user_endpoint import MobileUserSerializer
from dms.models.location import Location
from dms.models.mobile_user import MobileUser
from dms.tests.base import MongoTestCase


class MobileUserSerializerTest(MongoTestCase):
    def setUp(self):
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()

        self.serialized_location = dict(created_at=self.district.created_at, type=self.district.type,
                                        name=self.district.name, id=str(self.district.id))
        self.mobile_user = dict(name='timothy', phone='+256775019449', location=self.district,
                                email="timothyakampa@gmail.com")
        self.serialized_mobile_user = dict(name='timothy', phone='+256775019449', location=self.serialized_location,
                                           email="timothyakampa@gmail.com")

    def tearDown(self):
        MobileUser.drop_collection()
        Location.drop_collection()

    def test_should_serialize_mobile_user_object(self):
        mobile_user = MobileUser(**self.mobile_user).save()
        serialized_object = MobileUserSerializer(mobile_user)
        self.assertDictContainsSubset(self.serialized_mobile_user, serialized_object.data)
        self.assertIsNotNone(serialized_object.data['id'])

    def test_should_deserialize_mobile_user_object(self):
        self.serialized_mobile_user['location'] = self.district.id
        serializer = MobileUserSerializer(data=self.serialized_mobile_user)

        self.assertTrue(serializer.is_valid())
        saved_mobile_user = serializer.save()

        self.assertTrue(isinstance(saved_mobile_user, MobileUser))
        for attribute, value in self.mobile_user.items():
            self.assertEqual(value, getattr(saved_mobile_user, attribute))