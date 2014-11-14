import csv
import uuid
from django.core import management
from mongoengine.django.auth import Group, ContentType, Permission
from dms.models import User
from rest_framework.test import APITestCase
from django.test import TestCase
from dms import models as ALL_MODELS
import warnings
from django.utils.deprecation import RemovedInDjango18Warning


class MongoTestCase(TestCase):
    all_models = ALL_MODELS.__all__

    def login_user(self):
        user = User.objects.create(username='test_user', email='test@email.email')
        user.group = Group.objects(name='Administrator').first()
        user.set_password('password')
        self.client.login(username='test_user', password='password')

    def login_with_permission(self, permission_codename):
        self.client.logout()
        ct = ContentType(app_label='dms', model=str(uuid.uuid4()), name=str(uuid.uuid4())).save()
        permission = Permission(name=permission_codename, codename=permission_codename, content_type=ct.id).save()
        group = Group(name=str(uuid.uuid4()), permissions=[permission]).save()
        user = User(username='permitted', group=group)
        user.set_password('pw')
        self.client.login(username='permitted', password='pw')

    def login_without_permissions(self):
        self.client.logout()
        empty_group = Group(name='Empty', permissions=[])
        User(username='useless', password='pw', group=empty_group)
        self.client.login(username='useless', password='pw')

    def assert_permission_required_for_get(self, url):
        self.login_without_permissions()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

    def assert_permission_required_for_post(self, url):
        self.login_without_permissions()
        response = self.client.post(url)
        self.assertEquals(response.status_code, 403)

    def _fixture_setup(self):
        management.call_command('create_user_groups')
        warnings.filterwarnings("ignore", category=RemovedInDjango18Warning)
        pass

    def _fixture_teardown(self):
        pass

    def _post_teardown(self):
        self._flush_all_collections()
        super(MongoTestCase, self)._post_teardown()

    def _flush_all_collections(self):
        for model_str in self.all_models:
            model_class = getattr(ALL_MODELS, model_str)
            model_class.drop_collection()


class MongoAPITestCase(MongoTestCase, APITestCase):
    pass


class MongoTestWithCSV(MongoTestCase):

    def get_poll_response_csv_row(self, response):
        return "%s; %s; %s; %s" % (response.source(), response.text, response.location_str(), response.received_at)

    def write_to_csv(self, mode, data, csvfilename='test.csv'):
        with open(csvfilename, mode) as fp:
            file = csv.writer(fp, delimiter=',')
            file.writerows(data)
            fp.close()
