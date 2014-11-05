from rest_framework.response import Response
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListAPIView

from dms.models.user import User


class UserSerializer(serializers.MongoEngineModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'phone_no', 'location')


class UserListView(ListAPIView):
    def list(self, request, *args, **kwargs):
        user = User.objects(id=kwargs.get('user_id', None)).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
