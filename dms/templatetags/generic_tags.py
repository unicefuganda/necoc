from django import template
from dms.models import UserProfile

register = template.Library()

@register.filter
def get_profile_id(user):
    profile = UserProfile.objects(user=user).first()
    return profile.id if profile else ''