import datetime

from django.test import Client
from mongoengine.django.auth import User

from dms.models import Location, UserProfile, Poll, PollResponse
from dms.tests.base import MongoTestWithCSV


class ExportPollResponseViewTest(MongoTestWithCSV):
    def setUp(self):
        self.client = Client()
        date_time = datetime.datetime(2014, 9, 17, 16, 0, 49, 807000)
        phone_number = "+256775019449"

        self.district = Location(**dict(name='Kampala', parent=None, type='district')).save()
        self.village = Location(**dict(name='Bukoto', parent=self.district, type='village')).save()
        self.mobile_user = UserProfile(**dict(name='timothy', phone=phone_number, location=self.village, email=None)).save()
        self.mobile_user2 = UserProfile(**dict(name='timothy2', phone='12344', location=self.village, email=None)).save()

        poll_attr = dict(name="disaster space", question="How many disasters are in your area?", keyword="some_word",
                         target_locations=[str(self.village.id)])

        self.poll = Poll(**poll_attr).save()

        self.poll_response_attr = dict(phone_no=phone_number, text="NECOCPoll %s whatever"%self.poll['keyword'],
                                       received_at=date_time, relayer_id=234, run_id=23243, poll=self.poll)

        self.headings = "Respondent;Answer;Location;Responded on"

    def test_post_export_poll_response(self):
        poll_response = PollResponse(**self.poll_response_attr).save()
        poll_response_attr2 = self.poll_response_attr.copy()
        poll_response_attr2['text'] = "NECOCPoll %s whatever2"%self.poll['keyword']
        poll_response2 = PollResponse(**poll_response_attr2).save()

        self.login_user()
        response = self.client.get('/export/poll-responses/%s/'%str(self.poll.id))

        self.assertEquals(200, response.status_code)
        self.assertEquals(response.get('Content-Type'), 'text/csv')
        file_name = "disaster_space_responses.csv"
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename="%s"' % file_name)

        contents = "%s\r\n%s\r\n%s\r\n%s" % ("".join('sep=;'), "".join(self.headings), "".join(self.get_poll_response_csv_row(poll_response)),
                                       "".join(self.get_poll_response_csv_row(poll_response2)))
        self.assertEqual(contents, response.content)
