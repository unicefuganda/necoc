from dms.tests.base import MongoTestCase
from dms.utils.general_helpers import percentize, flatten, make_ratio


class GeneralHelperUtilsTest(MongoTestCase):

    def test_percentize(self):
        self.assertEqual(50, percentize(1, 2))
        self.assertEqual(0, percentize(0, 2))
        self.assertEqual(0, percentize(0, 0))

    def test_make_ratio(self):
        self.assertEqual(0.61, make_ratio(61, 100))
        self.assertEqual(0.50, make_ratio(1, 2))
        self.assertEqual(0, make_ratio(1, 0))
        self.assertEqual(0, make_ratio(0, 0))

    def test_flatten_list(self):
        list_=[[1,2,3],[4,5,6], [7], [8,9]]
        self.assertEqual([1,2,3,4,5,6,7,8,9], flatten(list_))

    def test_empty_is_discarded_when_flatten_list(self):
        list_=[[1,2],[], [4,5,6], [], [8,9]]
        self.assertEqual([1,2,4,5,6,8,9], flatten(list_))