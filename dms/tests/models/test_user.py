import uuid
from mongoengine.django.auth import Group, Permission, ContentType
from dms.models.user import User
from dms.tests.base import MongoTestCase


class TestUserModel(MongoTestCase):
    def test_has_group_permissions(self):
        ct = ContentType(app_label='dms', model='test', name='test').save()
        permission = Permission(name='can test things', codename='can_test_things', content_type=ct.id).save()
        group = Group(name='Test Group', permissions=[permission]).save()
        user = User(username='tim', password='password', group=group)
        self.assertTrue(user.has_perm('dms.can_test_things'))

    def test_does_not_have_group_permissions(self):
        ct = ContentType(app_label='dms', model='test', name='test').save()
        permission = Permission(name='can test things', codename='can_test_things', content_type=ct.id).save()
        group = Group(name='Test Group', permissions=[permission]).save()
        user = User(username='tim', password='password', group=group)
        self.assertFalse(user.has_perm('dmx.can_test_things'))
        self.assertFalse(user.has_perm('dms.cant_test_things'))

    def test_should_get_user_permissions(self):
        ct = ContentType(app_label='dms', model=str(uuid.uuid4()), name=str(uuid.uuid4())).save()
        manage_users = Permission(name='can manage users', codename='can_manage_users', content_type=ct.id).save()
        manage_polls = Permission(name='can manage users', codename='can_manage_polls', content_type=ct.id).save()
        group = Group(name='UserGroup', permissions=[manage_users, manage_polls]).save()
        user = User(username="some-name", email="some@email.com", group=group)
        user.set_password("some-password")

        self.assertEqual(['can_manage_users', 'can_manage_polls'], user.get_permissions())