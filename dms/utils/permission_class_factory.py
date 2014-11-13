from rest_framework import permissions


def build_permission_class(permission):
    return type(
        'DynamicPermissionClass',
        (permissions.BasePermission,),
        dict(
            has_permission=lambda self, request, view: request.user.has_perm(permission)
        )
    )
