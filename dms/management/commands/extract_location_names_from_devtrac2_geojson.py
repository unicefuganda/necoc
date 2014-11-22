import json
import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = 'name_of_the_csv.file'
    help = 'generates location hierarchy from geojson'

    def handle(self, *args, **kwargs):
        geojson_file = open(args[0], "r")
        geojson = json.loads(geojson_file.readline())
        data = self.get_location_names(geojson)
        self.write_to_csv('w', data, 'uganda_location_from_devtrac2.csv')
        self.stdout.write('Location Hierarchy Successfully Extracted!')

    @classmethod
    def get_location_names(cls, geojson):
        data = [['DistrictName', 'SubCountyName']]
        for feature in geojson.get('features'):
            data.append([feature['properties'].get('DNAME_2010', '*'), feature['properties'].get('SNAME_2010', '')])
        return data

    @classmethod
    def write_to_csv(cls, mode, data, csvfilename='test.csv'):
        with open(csvfilename, mode) as fp:
            file = csv.writer(fp, delimiter=',')
            file.writerows(data)
            fp.close()


