from django import template
from dms.models import UserProfile

register = template.Library()

@register.filter
def get_profile_id(user):
    profile = UserProfile.objects(user=user).first()
    return profile.id if profile else ''

@register.filter
def can_manage_settings(user):
    if user.group:
        if 'can_manage_settings' in user.get_permissions():
            return '<li><a id="admin_settings_link" href="#" data-toggle="modal" data-target="#admin-settings-modal">Manage Settings</a></li>'
        else:
            return ''
    else:
        return ''

@register.filter
def get_location_id(user):
    profile = UserProfile.objects(user=user).first()
    return profile.location.id if profile else ''