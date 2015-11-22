from dms.api.admin_setting_endpoint import AdminSettingSerializer
from dms.models import AdminSetting
from dms.tests.base import MongoTestCase


class AdminSettingSerializerTest(MongoTestCase):
    def setUp(self):

        self.admin_setting = dict(name="enable_first_setting")
        self.admin_setting_two = dict(name="count_another_thing", yes_no=False, value_int=10, value_str='')

    def test_should_serialize_admin_setting_object(self):
        admin_setting_object = AdminSetting(**self.admin_setting).save()
        serialized_data = AdminSettingSerializer(admin_setting_object)
        serialized_data_with_default_field_values = dict(self.admin_setting.items() +
                                           {'yes_no': True,
                                            'value_int': None,
                                            'value_str': None,
                                            }.items())
        self.assertEqual(serialized_data_with_default_field_values, serialized_data.data)

    def test_should_deserialize_admin_setting_object(self):
        serializer = AdminSettingSerializer(data=self.admin_setting_two)

        self.assertTrue(serializer.is_valid())

        saved_setting = serializer.save()

        self.assertTrue(isinstance(saved_setting, AdminSetting))
        for attribute, value in self.admin_setting_two.items():
            self.assertEqual(value, getattr(saved_setting, attribute))
