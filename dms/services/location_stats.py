from dms.models import RapidProMessage, Location, Disaster, DisasterType
from dms.utils.general_helpers import percentize, flatten


class LocationStatsAttribute(object):

    def __init__(self, object_class, location, **kwargs):
        self.attribute_class = object_class
        self.kwargs = kwargs
        self.queryset = self.get_queryset(location)

    def stats(self):
        attribute_count = self.attribute_count()
        total_attribute_count = self.attribute_class.count_(**self.kwargs)
        percentage = percentize(attribute_count, total_attribute_count)
        return StatsDetails(attribute_count, percentage)

    def attribute_count(self):
        return self.queryset.count()

    def get_queryset(self, location):
        if location:
            return self.attribute_class.from_(location=location, **self.kwargs)
        return self.attribute_class.objects().none()


class DisasterLocationStats(LocationStatsAttribute):

    def __init__(self, location, **kwargs):
        super(DisasterLocationStats, self).__init__(Disaster, location, **kwargs)

    def stats(self):
        location_stats = super(DisasterLocationStats, self).stats()
        affected = self.affected_areas()
        types = self.type_distribution()
        return DisasterStatsDetails(location_stats.count, location_stats.percentage, affected, types)

    def affected_areas(self):
        with_disasters = flatten(self.queryset.values_list('locations'))
        return len(set(with_disasters))

    def type_distribution(self):
        types = self.queryset.values_list('name').distinct('name')
        return {_type.name: self.queryset.filter(name=_type).count() for _type in types}


class LocationStatsService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def aggregate_stats(self):
        message_stats = LocationStatsAttribute(RapidProMessage, **self.kwargs).stats()
        disaster_stats = DisasterLocationStats(**self.kwargs).stats()
        return LocationStats(message_stats, disaster_stats)


class LocationStats(object):
    def __init__(self, messages=None, disasters=None):
        self.messages = messages
        self.disasters = disasters


class StatsDetails(object):
    def __init__(self, count, percentage):
        self.count = count
        self.percentage = percentage


class DisasterStatsDetails(StatsDetails):

    def __init__(self, count, percentage, affected_areas, type_distribution):
        super(DisasterStatsDetails, self).__init__(count, percentage)
        self.affected_areas = affected_areas
        self.type_distribution = type_distribution


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

