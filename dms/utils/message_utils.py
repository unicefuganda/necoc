from fuzzywuzzy import process
from django.conf import settings
from dms.models import Disaster


class MessageDisasterAssociator(object):
    def __init__(self, text):
        text = text or ''
        self.text = text

    def match_disaster(self):
        disasters = Disaster.objects.all()
        disasters = self._distinct([str(disaster) for disaster in disasters])
        match = process.extractOne(self.text, disasters)
        if match is None:
            return None
        return match[0] if (match[1] >= settings.DISASTER_ASSOCIATION_MATCH_RATIO) else None

    def _distinct(self, objs):
        distinct_list = []
        for obj in objs:
            if not obj in distinct_list:
                distinct_list.append(obj)
        return distinct_list
