from dms.models.location import Location
from dms.tests.base import NoSQLAPITestCase


class TestLocationEndpoint(NoSQLAPITestCase):

    LOCATION_ENDPOINT = '/api/v1/locations/'

    def setUp(self):
        self.district_to_post = dict(name='Kampala', type='district')
        self.district = dict(name='Kampala', type='district')
        self.expected_district = dict(name='Kampala', type="district", parent=None)

    def tearDown(self):
        Location.drop_collection()

    def test_should_post_a_location_without_a_parent(self):
        response = self.client.post(self.LOCATION_ENDPOINT, data=self.district_to_post)
        self.assertEqual(201, response.status_code)

        retrieved_location = Location.objects(**self.district)
        self.assertEqual(1, retrieved_location.count())

    def test_should_post_a_location_with_a_parent(self):
        response = self.client.post(self.LOCATION_ENDPOINT, data=self.district_to_post)
        saved_district_id = response.data['id']
        self.assertIsNotNone(saved_district_id)

        village_to_post = dict(name='Bukoto', type='village', parent=saved_district_id)
        response = self.client.post(self.LOCATION_ENDPOINT, data=village_to_post)
        self.assertEqual(201, response.status_code)

        retrieved_message = Location.objects(**village_to_post)
        self.assertEqual(1, retrieved_message.count())

    def test_should_get_a_list_of_locations(self):
        Location(**self.district).save()
        response = self.client.get(self.LOCATION_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(self.expected_district, response.data[0])

    def test_should_filter_locations_by_type(self):
        village = dict(name='Wakiso', type='village')
        Location(**self.district).save()
        Location(**village).save()

        response = self.client.get(self.LOCATION_ENDPOINT + '?type=district', format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(self.expected_district, response.data[0])

