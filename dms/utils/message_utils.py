import Levenshtein
from fuzzywuzzy import process
from django.conf import settings
from dms.models import Disaster, Location
from dms.utils.rapidpro_message_utils import split_text


class MessageDisasterAssociator(object):
    def __init__(self, text):
        text = text or ''
        self.text = text

    def match_disaster(self):
        disasters = Disaster.objects.all()
        return fuzzy_match_strings(self.text, disasters, settings.DISASTER_ASSOCIATION_MATCH_RATIO)


def location_ids(location_objects):
    locs = []
    for loc in location_objects:
        locs.append(loc.id)
    return locs


def distinct(objs):
    distinct_list = []
    for obj in objs:
        if not obj in distinct_list:
            distinct_list.append(obj)
    return distinct_list


def fuzzy_match_strings(var_str, strings_array, match_ratio=settings.DEFAULT_STR_MATCH_RATIO):
    _array = distinct([str(ustr) for ustr in strings_array])
    match = process.extractOne(var_str, _array)
    if match is None:
        return None
    return match[0] if (match[1] >= match_ratio) else None


class MessageProfileLocationAssociator(object):

    def __init__(self, mobile_user):
        self.mobile_user = mobile_user or None

    def best_match(self):
        if self.mobile_user:
            return self.mobile_user.location


class MessageTextLocationAssociator(object):

    def __init__(self, text):
        text = text or ''
        self.text = split_text(text)

    def best_match(self):
        if len(self.text) > settings.MESSAGE_LOCATION_INDEX + 1:
            location_name = self.text[settings.MESSAGE_LOCATION_INDEX]
            parent = self.get_first_location(parent=None)
            location = self.find_location_match(location_name, parent=parent)
            return location or self.get_first_location()

        if len(self.text) > settings.MESSAGE_LOCATION_INDEX - 1:
            return self.get_first_location()
        return None

    def get_first_location(self, **kwargs):
        location_name = self.text[settings.MESSAGE_LOCATION_INDEX-1]
        return self.find_location_match(location_name, **kwargs)

    @classmethod
    def find_location_match(cls, location_name, **kwargs):
        for location in Location.objects(**kwargs):
            ratio = Levenshtein.ratio(str(location.name).lower(), str(location_name).lower())
            if ratio >= settings.LOCATION_MATCH_LEVEL:
                return location

