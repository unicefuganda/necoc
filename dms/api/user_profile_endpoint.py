from django.contrib.auth.models import AnonymousUser
import re
from rest_condition import Or
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework_mongoengine.generics import ListCreateAPIView

from rest_framework_mongoengine import serializers
from rest_framework import serializers as rest_serializers
from rest_framework import fields
from rest_framework.response import Response
from dms.models import User

from dms.api.retrieve_update_wrapper import MongoRetrieveUpdateView
from dms.models.user_profile import UserProfile
from dms.services.user_profile_service import UserProfileService
from dms.utils.permission_class_factory import build_permission_class


class UserProfileSerializer(serializers.MongoEngineModelSerializer):
    username = fields.CharField(source='username', required=False)

    def validate_phone(self, attrs, source):
        phone = attrs.get(source)
        updated_value = phone != getattr(self.object, 'phone', '')
        self.__check_uniqueness(attrs, 'phone', UserProfile.objects(phone=phone), updated_value)
        return attrs

    def validate_email(self, attrs, source):
        email = attrs.get(source)
        updated_value = email != getattr(self.object, 'email', '')
        self.__check_uniqueness(attrs, 'email', UserProfile.objects(email=email), updated_value)
        return attrs

    def validate_username(self, attrs, source):
        username = attrs.get(source)
        updated_value = not (self.object and username == self.object.username())
        self.__check_uniqueness(attrs, 'username', User.objects(username=username), updated_value)
        return attrs

    def __check_uniqueness(self, attrs, field, objects_with_same_field_value, updated_value):
        if objects_with_same_field_value and updated_value:
            is_new_record = not attrs.get('id')
            has_non_unique_field_value = attrs.get('id') != objects_with_same_field_value.first().id
            if is_new_record or has_non_unique_field_value:
                raise rest_serializers.ValidationError(field.capitalize() + ' must be unique')

    class Meta:
        model = UserProfile
        exclude = ('created_at', 'user')


class UserProfileListCreateView(ListCreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects()
    model = UserProfile
    permission_classes = (build_permission_class('dms.can_manage_users'),)

    def pre_save(self, obj):
        username = self.request.DATA.get('username', None)
        if username:
            user = UserProfileService.setup_new_user(username, obj.name, obj.email)
            obj.user = user


class IsCurrentUsersProfile(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous():
            return False
        user_id = str(UserProfile.objects.get(user=request.user).id)
        return user_id in request.path


class UserProfileView(MongoRetrieveUpdateView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [Or(build_permission_class('dms.can_manage_users'), IsCurrentUsersProfile), ]

    def list(self, request, *args, **kwargs):
        user_profile = UserProfile.objects(id=kwargs['id']).first()
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)