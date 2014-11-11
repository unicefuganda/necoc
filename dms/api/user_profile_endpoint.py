from rest_framework_mongoengine.generics import ListCreateAPIView, ListAPIView
from rest_framework_mongoengine import serializers
from rest_framework import serializers as rest_serializers
from dms.api.retrieve_update_wrapper import MongoRetrieveUpdateView
from dms.models.user_profile import UserProfile
from rest_framework import fields
from rest_framework.response import Response
from dms.services.user_profile_service import UserProfileService


class UserProfileSerializer(serializers.MongoEngineModelSerializer):
    username = fields.CharField(source='username', required=False)

    def validate_phone(self, attrs, source):
        phone = attrs.get(source)
        profiles_with_same_phone = UserProfile.objects(phone=phone)
        if profiles_with_same_phone and getattr(self.object, 'phone', '') != phone:
            is_new_record = not (attrs.get('id'))
            has_non_unique_phone = attrs.get('id') != profiles_with_same_phone.first().id
            if is_new_record or has_non_unique_phone:
                raise rest_serializers.ValidationError('Phone number must be unique')

        return attrs

    def validate_email(self, attrs, source):
        email = attrs.get(source)
        profiles_with_same_email = UserProfile.objects(email=email)
        if profiles_with_same_email and getattr(self.object, 'email', '') != email:
            is_new_record = not (attrs.get('id'))
            has_non_unique_email = attrs.get('id') != profiles_with_same_email.first().id
            if is_new_record or has_non_unique_email:
                raise rest_serializers.ValidationError('Email must be unique')

        return attrs

    class Meta:
        model = UserProfile
        exclude = ('created_at', 'user')


class UserProfileListCreateView(ListCreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects()
    model = UserProfile

    def pre_save(self, obj):
        username = self.request.DATA.get('username', None)
        if username:
            user = UserProfileService.setup_new_user(username, obj.name, obj.email)
            obj.user = user


class UserProfileView(MongoRetrieveUpdateView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def list(self, request, *args, **kwargs):
        user_profile = UserProfile.objects(id=kwargs['id']).first()
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)