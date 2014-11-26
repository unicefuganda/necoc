from mongoengine.django.auth import Permission, ContentType, Group
from dms.tests.base import MongoAPITestCase


class GroupsEndpointTest(MongoAPITestCase):

    GROUPS_ENDPOINT = '/api/v1/groups/'

    def setUp(self):
        ct = ContentType(app_label='dms', model='test_ct', name='test_ct').save()
        self.permission = Permission(name='can manage something', codename='can_manage_something',
                                     content_type=ct.id).save()

    def test_should_get_groups_from_end_point(self):
        groups = Group.objects.all()
        response = self.client.get(self.GROUPS_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(groups.count(), len(response.data))

        for group in groups:
            self.assertIn(dict(id=str(group.id), name=group.name), response.data)

    def test_raise_403_if_user_doesnt_have_manage_user_permissions(self):
        self.assert_permission_required_for_post(self.GROUPS_ENDPOINT)