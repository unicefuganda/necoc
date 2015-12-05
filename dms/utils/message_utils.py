from fuzzywuzzy import process
from django.conf import settings
from dms.models import Disaster


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

