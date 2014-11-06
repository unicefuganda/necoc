import csv
from mongoengine.django.auth import User
from rest_framework.test import APITestCase
from django.test import TestCase
from dms import models as ALL_MODELS
import warnings
from django.utils.deprecation import RemovedInDjango18Warning


class MongoTestCase(TestCase):
    all_models = ALL_MODELS.__all__

    def login_user(self):
        user = User.objects.create(username='test_user', email='test@email.email')
        user.set_password('password')
        self.client.login(username='test_user', password='password')

    def _fixture_setup(self):
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
