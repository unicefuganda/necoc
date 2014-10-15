import Levenshtein
from django.conf import settings
from dms.models import Location


def find_location_match(location_name):
    for location in Location.objects():
        ratio = Levenshtein.ratio(str(location.name).lower(), str(location_name).lower())
        if ratio >= settings.LOCATION_MATCH_LEVEL:
            return location