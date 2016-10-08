__author__ = 'asseym'

from rest_framework.response import Response
from rest_framework_mongoengine.generics import ListAPIView
from dms.utils.user_profile_utils import get_user_district_coordinates


class CurrentCoordinatesView(ListAPIView):

    def list(self, request, *args, **kwargs):
        coordinates = get_user_district_coordinates(request.user)
        if len(coordinates):
            return Response({'lat': coordinates[1], 'long': coordinates[0]})
        else:
            return Response()
