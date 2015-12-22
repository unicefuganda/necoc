from django.conf import settings
from mongoengine import MultipleObjectsReturned, DoesNotExist
from dms.models import UserProfile

__author__ = 'asseym'


def get_profile(phone):
    return _mobile_user(phone)

def _mobile_user(phone):
    char_index = settings.NUMBER_OF_CHARS_IN_PHONE_NUMBER
    try:
        if len(phone) > char_index:
            mobile_user = UserProfile.objects.get(phone__endswith=phone[-1*char_index:len(phone)])
        else:
            mobile_user = UserProfile.objects.get(phone=phone)
        return mobile_user
    except MultipleObjectsReturned:
        if len(phone) > char_index:
            mobile_user = UserProfile.objects(phone__endswith=phone[-1*char_index:len(phone)]).first()
        else:
            mobile_user = UserProfile.objects(phone=phone).first()
        return mobile_user
    except DoesNotExist:
        return None
    except TypeError:
        return None
