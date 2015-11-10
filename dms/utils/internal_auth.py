__author__ = 'asseym'

from django.middleware import csrf
from dms.models import User
from rest_framework import authentication
from rest_framework import exceptions


class InternalCallAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_API_USER')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)

        # if self._check_csrf():
        #     return (user, None)
        # else:
        #     return None

    def _check_csrf(request):
        reason = csrf.CsrfViewMiddleware().process_view(request, None, (), {})
        if reason:
            # CSRF failed
            raise csrf.PermissionException()
