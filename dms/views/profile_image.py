from django.http import HttpResponse
from rest_condition import Or
from rest_framework_mongoengine.generics import MongoAPIView
from dms.api.user_profile_endpoint import IsCurrentUsersProfile
from dms.models import UserProfile
from dms.utils.permission_class_factory import build_permission_class
from necoc import settings


class ProfileImageView(MongoAPIView):
    permission_classes = [Or(build_permission_class('dms.can_manage_users'), IsCurrentUsersProfile), ]
    DEFAULT_IMAGE_PATH = settings.STATICFILES_DIRS[0] + "/img/default_profile.jpg"

    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(id=kwargs['id'])
            if profile and hasattr(profile, 'photo'):
                photo = profile.photo.read()
                return HttpResponse(photo, content_type=profile.photo.content_type)
        except:
            return HttpResponse(open(self.DEFAULT_IMAGE_PATH), content_type='image/jpeg')
