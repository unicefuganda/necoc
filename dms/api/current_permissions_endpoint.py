from rest_framework.response import Response
from rest_framework_mongoengine.generics import ListAPIView


class CurrentPermissionsView(ListAPIView):

    def list(self, request, *args, **kwargs):
        return Response({'permissions': request.user.get_permissions()})