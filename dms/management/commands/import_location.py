from django.core.management.base import BaseCommand, CommandError
from dms.models.location import Location
import csv


class Command(BaseCommand):
    args = 'name_of_the_csv.file'
    help = 'Populates locations from a csv file'

    def handle(self, *args, **kwargs):
        csv_file = csv.reader(open(args[0], "rb"))
        headers = csv_file.next()
        location_types = self._location_types(headers)
        for items in csv_file:
            parent = None
            for index, item in enumerate(items):
                parent = Location.objects.get_or_create(name=item.strip(), type=location_types[index], parent=parent)[0]
        self.stdout.write('Successfully imported!')

    def _location_types(self, headers):
        type_choices = [choice[0] for choice in Location.TYPE_CHOICES]
        headers = map(lambda header: header.strip().replace("Name", "").lower(), headers)
        return filter(lambda header: header in type_choices, headers)
