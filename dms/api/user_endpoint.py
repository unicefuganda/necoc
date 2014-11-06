from rest_framework.response import Response
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListAPIView

from dms.models.user import User


class UserSerializer(serializers.MongoEngineModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_no', 'location')


class UserListView(ListAPIView):

    def list(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id', '')
        user = User.objects(id=user_id).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
