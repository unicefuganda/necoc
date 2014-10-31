from django.http import HttpResponse
from django.views.generic import View

from dms.models import Poll
from dms.services.export_poll_responses import ExportPollResponsesService


class ExportPollResponsesView(View):

    def get(self, *args, **kwargs):
        poll_id = kwargs['poll_id']
        poll = Poll.objects.get(id=poll_id)
        export_service = ExportPollResponsesService(poll)
        formatted_responses = export_service.get_formatted_responses()
        response = HttpResponse(content_type='text/csv')
        poll_name = poll.name
        response['Content-Disposition'] = 'attachment; filename="%s_responses.csv"' % poll_name.replace(" ", "_")
        response.write("\r\n".join(formatted_responses))
        return response

