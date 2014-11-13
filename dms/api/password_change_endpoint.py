from mongoengine.django.auth import User
from rest_framework_mongoengine import serializers
from rest_framework import serializers as rest_serializers


class UserPasswordChangeSerializer(serializers.MongoEngineModelSerializer):
    old_password = rest_serializers.CharField()
    new_password = rest_serializers.CharField()
    confirm_password = rest_serializers.CharField()

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


