from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from dms.models.mobile_user import MobileUser


class MobileUserSerializer(serializers.MongoEngineModelSerializer):
    class Meta:
        model = MobileUser
        exclude = ('created_at',)


class MobileUserListCreateView(ListCreateAPIView):
    serializer_class = MobileUserSerializer
    queryset = MobileUser.objects()
    model = MobileUser