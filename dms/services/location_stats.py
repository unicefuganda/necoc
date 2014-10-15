from dms.models import RapidProMessage, Location
from dms.utils.general_helpers import percentize


class LocationStatsService(object):

    def __init__(self, location):
        self.location = location
        self.total_message_count = RapidProMessage.objects.count()

    def aggregate_stats(self):
        message_stats = self.message_stats()
        return LocationStats(message_stats)

    def message_stats(self):
        message_count = self.message_count()
        percentage = percentize(message_count, self.total_message_count)
        return StatsDetails(message_count, percentage)

    def message_count(self):
        if self.location:
            return RapidProMessage.from_(self.location).count()
        return 0


class LocationStats(object):
    def __init__(self, messages, disasters=None):
        self.messages = messages
        self.disasters = disasters


class StatsDetails(object):
    def __init__(self, count, percentage):
        self.count = count
        self.percentage = percentage


class MultiLocationStatsService(object):

    def stats(self):
        districts = Location.objects(parent=None)
        return {location.name: LocationStatsService(location).aggregate_stats() for location in districts}
