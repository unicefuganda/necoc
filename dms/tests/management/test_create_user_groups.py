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


class CreateUserGroupsTest(MongoTestCase):

    def setUp(self):
        self.kampala = Location(name='Kampala', type='district').save()

    def test_should_create_default_superuser(self):
        pass