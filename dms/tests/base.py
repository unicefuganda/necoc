import csv
from rest_framework.test import APITestCase
from django.test import TestCase
from dms import models as ALL_MODELS


class MongoTestCase(TestCase):
    all_models = ALL_MODELS.__all__

    def _fixture_setup(self):
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

    def write_to_csv(self, mode, data, csvfilename='test.csv'):
        with open(csvfilename, mode) as fp:
            file = csv.writer(fp, delimiter=',')
            file.writerows(data)
            fp.close()
