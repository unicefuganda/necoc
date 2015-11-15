from necoc import settings
from dms.models import User
from rest_framework import authentication

__author__ = 'asseym'


class InternalCallAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        step = request.DATA.get('step')
        if step == settings.API_AUTHORIZED_STEP:
            username = User.objects.order_by('-created_at').first()
        if not username:
            return None

        return (username, None)
