from mongoengine.django.auth import check_password, User
from dms.management.commands.create_super_user import Command
from dms.models import UserProfile, Location
from dms.tests.base import MongoTestCase


class FakeStdout(object):
    def write(self, msg):
        return "--%s" % msg


class FakeCommand(Command):
    def __init__(self):
        super(FakeCommand, self).__init__()
        self.stdout = FakeStdout()


class CreateSuperuserTest(MongoTestCase):
    def setUp(self):
        self.kampala = Location(name='Kampala', type='district').save()

    def test_should_create_default_superuser(self):
        FakeCommand().handle()
        self.assertEqual(1, User.objects().count())
        user = User.objects().first()
        user_profile = UserProfile.objects().first()
        self.assertEqual('admin', user.username)
        self.assertTrue(check_password('password', user.password))
        self.assertNotEqual('password', user.password)
        self.assertEqual('admin@admin.admin', user_profile.email)
        self.assertEqual(self.kampala, user_profile.location)
        self.assertEqual('N/A', user_profile.phone)
        self.assertEqual('Admin', user_profile.name)

    def test_should_handle_existing_profile(self):
        UserProfile(phone='N/A', name='Admin', location=self.kampala, email='admin@admin.admin').save()
        FakeCommand().handle()
        self.assertEqual(1, User.objects().count())
        user = User.objects().first()
        user_profile = UserProfile.objects().first()
        self.assertEqual('admin', user.username)
        self.assertTrue(check_password('password', user.password))
        self.assertNotEqual('password', user.password)
        self.assertEqual('admin@admin.admin', user_profile.email)
        self.assertEqual(self.kampala, user_profile.location)
        self.assertEqual('N/A', user_profile.phone)
        self.assertEqual('Admin', user_profile.name)

    def test_should_create_super_user_from_args(self):
        FakeCommand().handle('new_admin',
                             'new_password',
                             'new_admin@admin.admin',
                             'NewAdmin',
                             'Kampala',
                             '1234567890')
        self.assertEqual(1, User.objects().count())
        user = User.objects().first()
        user_profile = UserProfile.objects().first()
        self.assertEqual('new_admin', user.username)
        self.assertTrue(check_password('new_password', user.password))
        self.assertNotEqual('new_password', user.password)
        self.assertEqual('new_admin@admin.admin', user_profile.email)
        self.assertEqual(self.kampala, user_profile.location)
        self.assertEqual('1234567890', user_profile.phone)
        self.assertEqual('NewAdmin', user_profile.name)

    def test_should_handle_existing_profile_from_args(self):
        UserProfile(phone='1234567890', name='NewAdmin', location=self.kampala, email='new_admin@admin.admin').save()
        FakeCommand().handle('new_admin',
                             'new_password',
                             'new_admin@admin.admin',
                             'NewAdmin',
                             'Kampala',
                             '1234567890')
        self.assertEqual(1, User.objects().count())
        user = User.objects().first()
        user_profile = UserProfile.objects().first()
        self.assertEqual('new_admin', user.username)
        self.assertTrue(check_password('new_password', user.password))
        self.assertNotEqual('new_password', user.password)
        self.assertEqual('new_admin@admin.admin', user_profile.email)
        self.assertEqual(self.kampala, user_profile.location)
        self.assertEqual('1234567890', user_profile.phone)
        self.assertEqual('NewAdmin', user_profile.name)
