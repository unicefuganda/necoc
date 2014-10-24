import os

from dms.models.location import Location
from dms.management.commands.import_location import Command
from dms.tests.base import MongoTestWithCSV


class FakeStdout(object):
    def write(self, msg):
        return "haha %s"%msg


class FakeCommand(Command):
    def __init__(self):
        super(FakeCommand, self).__init__()
        self.stdout = FakeStdout()


class ImportLocationTest(MongoTestWithCSV):
    def setUp(self):
        self.data = [['DistrictName', 'SubcountyName'],
                     ['district1', 'Subcounty1'],
                     ['district2', 'Subcounty2']]

        self.write_to_csv('wb', self.data)
        self.filename = 'test.csv'
        file = open(self.filename, 'rb')
        self.importer = FakeCommand()

    def tearDown(self):
        os.system("rm -rf %s"%self.filename)

    def test_should_create_locations(self):
        self.importer.handle(self.filename)
        types = [type_name.replace('Name', '') for type_name in self.data[0]]
        for locations in self.data[1:]:
            [self.failUnless(Location.objects.filter(name=location_name, type__iexact=types[index].lower())) for
             index, location_name in enumerate(locations)]

    def test_should_respect_locations_hierarchy(self):
        self.importer.handle(self.filename)
        for locations in self.data[1:]:
            for index, location_name in enumerate(locations[:-2]):
                parent = Location.objects.get(name=location_name)
                self.assertEqual(parent, Location.objects.get(name=locations[index+1]).parent)
