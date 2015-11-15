from necoc import settings
from dms.models import User
from rest_framework import authentication

__author__ = 'asseym'


class InternalCallAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        print request.DATA
        step = request.DATA.get('step')
        user = User.objects.order_by('-created_at').first()
        if step == settings.API_AUTHORIZED_STEP:
            return (user, None)
        else:
            return None

