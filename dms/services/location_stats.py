from dms.models import RapidProMessage, Location, Disaster
from dms.utils.general_helpers import percentize


class LocationStatsAttribute(object):

    def __init__(self, object_class, location, **kwargs):
        self.location = location
        self.attribute_class = object_class
        self.kwargs = kwargs

    def stats(self):
        attribute_count = self.attribute_count()
        total_attribute_count = self.attribute_class.count_(**self.kwargs)
        percentage = percentize(attribute_count, total_attribute_count)
        return StatsDetails(attribute_count, percentage)

    def attribute_count(self):
        if self.location:
            return self.attribute_class.from_(location=self.location, **self.kwargs).count()
        return 0


class LocationStatsService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def aggregate_stats(self):
        message_stats = LocationStatsAttribute(RapidProMessage, **self.kwargs).stats()
        disaster_stats = LocationStatsAttribute(Disaster, **self.kwargs).stats()
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
    def __init__(self, location, **kwargs):
        self.location_name = location
        self.locations = self.set_locations()
        self.kwargs = kwargs

    def stats(self):
        return {location.name: LocationStatsService(location=location, **self.kwargs).aggregate_stats() for
                location in self.locations}

    def set_locations(self):
        if self.location_name:
            location = Location.objects.filter(name__iexact=self.location_name).first()
            if location:
                return location.children()
        return Location.objects(parent=None)

