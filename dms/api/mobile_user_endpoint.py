from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from rest_framework import serializers as rest_serializers
from dms.models.mobile_user import MobileUser


class MobileUserSerializer(serializers.MongoEngineModelSerializer):
    def validate_phone(self, attrs, source):
        if len(MobileUser.objects(phone=attrs[source])):
            raise rest_serializers.ValidationError('Phone number must be unique')
        return attrs

    def validate_email(self, attrs, source):
        email = attrs.get(source, None)
        if email and MobileUser.objects(email=email):
            raise rest_serializers.ValidationError('Email must be unique')
        return attrs

    class Meta:
        model = MobileUser
        exclude = ('created_at',)


class MobileUserListCreateView(ListCreateAPIView):
    serializer_class = MobileUserSerializer
    queryset = MobileUser.objects()
    model = MobileUser