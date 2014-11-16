from mongoengine.django.auth import Permission, ContentType, Group
from dms.tests.base import MongoAPITestCase


class GroupsEndpointTest(MongoAPITestCase):

    GROUPS_ENDPOINT = '/api/v1/groups/'

    def setUp(self):
        ct = ContentType(app_label='dms', model='test_ct', name='test_ct').save()
        self.permission = Permission(name='can manage something', codename='can_manage_something',
                                     content_type=ct.id).save()

    def test_should_get_groups_from_end_point(self):
        Group.drop_collection()
        group = Group(name='Test Group', permissions=[self.permission]).save()
        response = self.client.get(self.GROUPS_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(dict(id=str(group.id), name='Test Group'), response.data[0])