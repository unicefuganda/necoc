from dms.models import RapidProMessage, Location


class LocationStatsService(object):

    def __init__(self, location_name):
        self.location = Location.objects(name__iexact=location_name.lower()).first()

    def aggregate_stats(self):
        return {'messages': self.message_stats()}

    def message_stats(self):
        if self.location:
            return RapidProMessage.from_(self.location).count()
        return 0