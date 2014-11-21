import Levenshtein
from django.conf import settings
from dms.models import Location
from dms.utils.rapidpro_message_utils import split_text


class MessageLocationExtractor(object):

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

