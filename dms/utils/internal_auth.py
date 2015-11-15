from necoc import settings
from dms.models import User
from rest_framework import authentication
import urlparse

__author__ = 'asseym'


class InternalCallAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        import pdb;pdb.set_trace()
        query_string = request.META.get('QUERY_STRING')
        query_dict = self.parse_query_string(query_string)
        user = User.objects.order_by('-created_at').first()
        if query_dict['step'] == settings.API_AUTHORIZED_STEP:
            return (user, None)
        else:
            return None


    def parse_query_string(self, query_string):
        return dict(urlparse.parse_qsl(query_string))


