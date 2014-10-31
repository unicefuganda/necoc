from dms.models import PollResponse


class ExportPollResponsesService(object):
    HEADERS = "Respondent;Answer;Location;Responded on"

    def __init__(self, poll):
        self.poll = poll
        self.responses = PollResponse.objects(poll=self.poll)

    def get_formatted_responses(self):
        formatted_responses = [self.export_format(response) for response in self.responses]
        formatted_responses.insert(0, self.HEADERS)
        return formatted_responses

    def export_format(self, response):
        return "%s; %s; %s; %s" % (response.source(), response.text, response.location_str(), response.received_at)
