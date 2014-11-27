from rest_framework import permissions
from rest_framework.permissions import BasePermission
from dms.models import UserProfile


class IsGetRequest(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'


class UrlMatchesCurrentUser(BasePermission):
    def has_permission(self, request, view):
        profile = UserProfile.objects(user=request.user).first()
        return profile is not None and str(profile.id) in request.path


class LoggedIn(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active


def build_permission_class(permission):
    return type(
        'DynamicPermissionClass',
        (permissions.BasePermission,),
        dict(
            has_permission=lambda self, request, view: request.user.has_perm(permission)
        )
    )
