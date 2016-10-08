from django.core.management.base import BaseCommand, CommandError
from dms.models.location import Location
import json
from pprint import pprint


class Command(BaseCommand):
    args = 'name_of_the_json.file'
    help = 'Populates locations with coordinates'

    def handle(self, *args, **kwargs):

        with open(args[0]) as data_file:
            data = json.load(data_file)
        for feature in data["features"]:
            dist_name = feature["properties"]["DNAME_2010"]
            dist_coordinates = feature["geometry"]["coordinates"][0][0]
            loc = Location.objects.get(type='district', name__iexact=dist_name)
            loc.latlong = dist_coordinates
            loc.save()
        self.stdout.write('Successfully imported!')
