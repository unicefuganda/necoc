from mongoengine.django.auth import User
from rest_framework_mongoengine.generics import ListCreateAPIView, ListAPIView
from rest_framework_mongoengine import serializers
from rest_framework import serializers as rest_serializers
from dms.models.user_profile import UserProfile
from rest_framework import fields
from rest_framework.response import Response


class UserProfileSerializer(serializers.MongoEngineModelSerializer):
    username = fields.CharField(source='username', required=False)

    def validate_phone(self, attrs, source):
        if len(UserProfile.objects(phone=attrs[source])):
            raise rest_serializers.ValidationError('Phone number must be unique')
        return attrs

    def validate_email(self, attrs, source):
        email = attrs.get(source, None)
        if email and UserProfile.objects(email=email):
            raise rest_serializers.ValidationError('Email must be unique')
        return attrs

    class Meta:
        model = UserProfile
        exclude = ('created_at', 'user')


class UserProfileListCreateView(ListCreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects()
    model = UserProfile

    def __init__(self, *args, **kwargs):
        self.user = None
        return super(UserProfileListCreateView, self).__init___(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        if username:
            self.user = User(username=username).save()
        return super(UserProfileListCreateView, self).post(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.user = self.user
        return super(UserProfileListCreateView, self).pre_save(obj)


class UserProfileView(ListAPIView):
    def list(self, request, *args, **kwargs):
        user_profile = UserProfile.objects(id=kwargs['id']).first()
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

