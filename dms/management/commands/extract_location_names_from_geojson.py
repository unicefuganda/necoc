import json
import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = 'name_of_the_csv.file DNAME_2010 SNAME_2010'
    help = 'generates location hierarchy from geojson'

    def handle(self, *args, **kwargs):
        geojson_file = open(args[0], "r")
        geojson = json.loads(geojson_file.readline())
        district_attribute = args[1] if len(args) > 1 else 'DNAME2014'
        subcounty_attribute = args[2] if len(args) > 2 else 'SNAME2014'
        data = self.get_location_names(geojson, district_attribute, subcounty_attribute)
        self.write_to_csv('w', data, args[0].replace('json', 'csv'))
        self.stdout.write('Location Hierarchy Successfully Extracted!')

    @classmethod
    def get_location_names(cls, geojson, district_attribute, subcounty_attribute):
        data = [['DistrictName', 'SubCountyName']]
        for feature in geojson.get('features'):
            data.append([feature['properties'].get(district_attribute, '*'), feature['properties'].get(subcounty_attribute, '')])
        return data

    @classmethod
    def write_to_csv(cls, mode, data, csvfilename='test.csv'):
        with open(csvfilename, mode) as fp:
            file = csv.writer(fp, delimiter=',')
            file.writerows(data)
            fp.close()


