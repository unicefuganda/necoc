from mongoengine.django.auth import User, check_password
from dms.management.commands.create_super_user import Command
from dms.tests.base import MongoTestCase


class FakeStdout(object):
    def write(self, msg):
        return "--%s" % msg


class FakeCommand(Command):
    def __init__(self):
        super(FakeCommand, self).__init__()
        self.stdout = FakeStdout()


class CreateSuperuserTest(MongoTestCase):
    def test_should_create_default_superuser(self):
        FakeCommand().handle()
        self.assertEqual(1, User.objects().count())
        user = User.objects().first()
        self.assertEqual('admin', user.username)
        self.assertTrue(check_password('password', user.password))
        self.assertNotEqual('password', user.password)
        self.assertEqual('admin@admin.admin', user.email)

    def test_should_create_super_user_from_args(self):
        FakeCommand().handle('not_admin', 'not_password', 'not_admin@admin.admin')
        self.assertEqual(1, User.objects().count())
        user = User.objects().first()
        self.assertEqual('not_admin', user.username)
        self.assertTrue(check_password('not_password', user.password))
        self.assertNotEqual('not_password', user.password)
        self.assertEqual('not_admin@admin.admin', user.email)
