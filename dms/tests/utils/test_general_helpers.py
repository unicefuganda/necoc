from dms.tests.base import MongoTestCase
from dms.utils.general_helpers import percentize


class GeneralHelperUtilsTest(MongoTestCase):

    def test_percentize(self):
        self.assertEqual(50, percentize(1, 2))
        self.assertEqual(0, percentize(0, 2))
        self.assertEqual(0, percentize(0, 0))