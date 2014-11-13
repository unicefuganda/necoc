from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsGetRequest(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'


def build_permission_class(permission):
    return type(
        'DynamicPermissionClass',
        (permissions.BasePermission,),
        dict(
            has_permission=lambda self, request, view: request.user.has_perm(permission)
        )
    )
