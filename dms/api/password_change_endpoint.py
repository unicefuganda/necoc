from dms.models import User
from rest_framework_mongoengine.generics import UpdateAPIView
from rest_framework_mongoengine import serializers
from rest_framework import serializers as rest_serializers

from dms.models.user_profile import UserProfile
from dms.services.user_profile_service import UserProfileService


class UserPasswordChangeSerializer(serializers.MongoEngineModelSerializer):
    old_password = rest_serializers.CharField(write_only=True)
    new_password = rest_serializers.CharField(write_only=True)
    confirm_password = rest_serializers.CharField(write_only=True)

    def validate_old_password(self, attrs, source):
        old_password = attrs.get(source)
        if not self.object.check_password(old_password):
            raise rest_serializers.ValidationError('Current password incorrect.')
        return attrs

    def validate_confirm_password(self, attrs, source):
        confirm_password = attrs.get(source)
        new_password = attrs.get('new_password')
        if new_password and confirm_password and (new_password != confirm_password):
            raise rest_serializers.ValidationError("The two password fields didn't match.")
        return attrs

    def restore_object(self, attrs, instance=None):
        self.object.set_password(attrs['new_password'])
        return self.object

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password', )


class PasswordChangeView(UpdateAPIView):
    serializer_class = UserPasswordChangeSerializer
    queryset = UserProfile.objects()
    model = UserProfile

    def get_object(self, queryset=None):
        profile = super(PasswordChangeView, self).get_object()
        if not profile.user:
            from django.http import Http404
            raise Http404('%s is not a web user.' % profile.name)
        return profile.user

    def pre_save(self, obj):
        profile = super(PasswordChangeView, self).get_object()
        UserProfileService(profile).notify_password_change()

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
