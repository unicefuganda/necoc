from dms.models.location import Location
from dms.tests.base import MongoAPITestCase


class TestLocationEndpoint(MongoAPITestCase):

    LOCATION_ENDPOINT = '/api/v1/locations/'

    def setUp(self):
        self.district_to_post = dict(name='Kampala', type='district')
        self.district = dict(name='Kampala', type='district')
        self.expected_district = dict(name='Kampala', type="district", parent=None)

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

    def test_should_filter_locations_by_parent(self):
        kampala = Location(**self.district).save()
        village = dict(name='Wakiso', type='village')
        Location(parent=kampala, **village).save()

        response = self.client.get(self.LOCATION_ENDPOINT, {"parent": kampala.id, "format":"json"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(village, response.data[0])

    def test_should_filter_locations_by_no_parent(self):
        kampala = Location(**self.district).save()
        village = dict(name='Wakiso', type='village', parent=kampala.id)
        Location(**village).save()

        response = self.client.get(self.LOCATION_ENDPOINT +"?parent=&format=json")

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictContainsSubset(self.expected_district, response.data[0])


class TestLocationChildrenEndpoint(MongoAPITestCase):

    LOCATION_ENDPOINT = '/api/v1/locations/'

    def setUp(self):
        self.district_to_post = dict(name='Kampala', type='district')
        self.district = dict(name='Kampala', type='district')

        self.kampala = Location(**self.district).save()
        self.wakiso_attr = dict(name='Wakiso', type='county', parent=self.kampala.id)
        self.masaka_attr = dict(name='masaka', type='county')

        self.wakiso = Location(**self.wakiso_attr).save()
        self.masaka = Location(**self.masaka_attr).save()

    def test_should_filter_location_children_by_district_location_type(self):
        response = self.client.get(self.LOCATION_ENDPOINT + "?district=%s&type=county&format=json" % self.kampala.id)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))

        self.wakiso_attr['id'] = str(self.wakiso.id)

        for key in ['id', 'name', 'type']:
            self.assertEqual(self.wakiso_attr[key], response.data[0][key])

    def test_should_filter_location_children_by_county_location_type(self):
        wakiso_subcounty_attr = dict(name='Wakiso Subcounty', type='subcounty', parent=self.wakiso.id)
        masaka_subcounty_attr = dict(name='masaka Subcounty', type='subcounty', parent=self.masaka.id)
        wakiso_subcounty = Location(**wakiso_subcounty_attr).save()
        masaka_subcounty = Location(**masaka_subcounty_attr).save()

        response = self.client.get(self.LOCATION_ENDPOINT + "?county=%s&type=subcounty&format=json" % self.wakiso.id)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))

        wakiso_subcounty_attr['id'] = str(wakiso_subcounty.id)

        for key in ['id', 'name', 'type']:
            self.assertEqual(wakiso_subcounty_attr[key], response.data[0][key])

    def test_county_cannot_be_parent_of_district(self):
        response = self.client.get(self.LOCATION_ENDPOINT + "?county=%s&type=district&format=json" % self.wakiso.id)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

    def test_all_location_type(self):

        response = self.client.get(self.LOCATION_ENDPOINT + "?county=%s&type=subcounty&format=json" % self.wakiso.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

        response = self.client.get(self.LOCATION_ENDPOINT + "?subcounty=%s&type=parish&format=json" % self.wakiso.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

        response = self.client.get(self.LOCATION_ENDPOINT + "?parish=%s&type=village&format=json" % self.wakiso.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.data))

