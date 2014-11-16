from mongoengine.django.auth import ContentType, Permission, Group
from dms.api.groups_endpoint import GroupSerializer
from dms.tests.base import MongoTestCase


class GroupSerializerTest(MongoTestCase):
    def setUp(self):
        ct = ContentType(app_label='dms', model='test_ct', name='test_ct').save()
        self.permission = Permission(name='can manage something', codename='can_manage_something',
                                     content_type=ct.id).save()

    def test_should_serialize_groups_object(self):
        serialized_group = dict(name='Test Group')
        group_object = Group(name='Test Group', permissions=[self.permission]).save()

        serialized_object = GroupSerializer(group_object)
        self.assertDictContainsSubset(serialized_group, serialized_object.data)
        self.assertIsNotNone(serialized_object.data.get('id'))
        self.assertIsNone(serialized_object.data.get('permission'))