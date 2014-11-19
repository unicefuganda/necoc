from dms.models import Disaster
from dms.utils.general_helpers import flatten


class SummaryStatsAttribute(object):

    def __init__(self, object_class, location, **kwargs):
        self.attribute_class = object_class
        self.kwargs = kwargs
        self.queryset = self.get_queryset(location)

    def stats(self):
        counts = self.attribute_count()
        affected = self.affected_areas()
        types = self.type_distribution()
        return SummaryStatsDetails(counts, affected, types)

    def attribute_count(self):
        return self.queryset.count()

    def affected_areas(self):
        with_disasters = flatten(self.queryset.values_list('locations'))
        return len(set(with_disasters))

    def type_distribution(self):
        types = self.queryset.values_list('name').distinct('name')
        return {_type.name: self.queryset.filter(name=_type).count() for _type in types}

    def get_queryset(self, location):
        if location:
            return self.attribute_class.from_(location=location, **self.kwargs)
        return self.attribute_class.objects(**self.kwargs)


class SummaryStats(object):
    def __init__(self, disasters=None):
        self.disasters = disasters


class SummaryStatsDetails(object):
    def __init__(self, count, affected_areas, type_distribution):
        self.count = count
        self.affected = affected_areas
        self.types = type_distribution


class StatsSummaryService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def aggregate_stats(self):
        disaster_stats = SummaryStatsAttribute(Disaster, **self.kwargs).stats()
        return SummaryStats(disaster_stats)
