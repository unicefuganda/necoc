import datetime

from dms.models import Location, MobileUser, Poll, PollResponse
from dms.services.export_poll_responses import ExportPollResponsesService
from dms.tests.base import MongoTestWithCSV


class ExportPollResponseServiceTest(MongoTestWithCSV):

    def setUp(self):
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"

        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = MobileUser(**dict(name='timothy', phone=phone_number, location=self.village, email=None)).save()
        self.mobile_user2 = MobileUser(**dict(name='timothy2', phone='12344', location=self.village, email=None)).save()

        poll_attr = dict(name="Disaster", question="How many disasters are in your area?", keyword="some_word",
                         target_locations=[str(self.village.id)])

        self.poll = Poll(**poll_attr).save()

        self.poll_response_attr = dict(phone_no=phone_number, text="NECOCPoll %s whatever"%self.poll['keyword'],
                                       received_at=date_time, relayer_id=234, run_id=23243, poll=self.poll)

        self.headings = "Respondent;Answer;Location;Responded on"

    def test_exports_poll_responses(self):
        response = PollResponse(**self.poll_response_attr).save()
        poll_response_attr2 = self.poll_response_attr.copy()
        poll_response_attr2['text'] = "NECOCPoll %s whatever2"%self.poll['keyword']
        response2 = PollResponse(**poll_response_attr2).save()

        expected_data = [self.headings, self.get_poll_response_csv_row(response), self.get_poll_response_csv_row(response2)]

        export_poll_service = ExportPollResponsesService(self.poll)
        actual_data = export_poll_service.get_formatted_responses()

        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)
        self.assertIn(expected_data[1], actual_data)
        self.assertIn(expected_data[2], actual_data)
