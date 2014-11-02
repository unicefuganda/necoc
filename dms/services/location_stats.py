from dms.models import RapidProMessage, Location, Disaster
from dms.utils.general_helpers import percentize


class LocationStatsAttribute(object):

    def __init__(self, location, object_class):
        self.location = location
        self.attribute_class = object_class

    def stats(self):
        attribute_count = self.attribute_count()
        total_attribute_count = self.attribute_class.objects.count()
        percentage = percentize(attribute_count, total_attribute_count)
        return StatsDetails(attribute_count, percentage)

    def attribute_count(self):
        if self.location:
            return self.attribute_class.from_(self.location).count()
        return 0


class LocationStatsService(object):

    def __init__(self, location):
        self.location = location

    def aggregate_stats(self):
        message_stats = LocationStatsAttribute(self.location, RapidProMessage).stats()
        disaster_stats = LocationStatsAttribute(self.location, Disaster).stats()
        return LocationStats(message_stats, disaster_stats)


class LocationStats(object):
    def __init__(self, messages=None, disasters=None):
        self.messages = messages
        self.disasters = disasters


class StatsDetails(object):
    def __init__(self, count, percentage):
        self.count = count
        self.percentage = percentage


class MultiLocationStatsService(object):

    def __init__(self, location=None):
        self.location_name = location
        self.locations = self.set_locations()

    def stats(self):
        return {location.name: LocationStatsService(location).aggregate_stats() for location in self.locations}

    def set_locations(self):
        if self.location_name:
            location = Location.objects.filter(name__iexact=self.location_name).first()
            if location:
                return location.children()
        return Location.objects(parent=None)

