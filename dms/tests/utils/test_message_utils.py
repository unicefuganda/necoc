from django.test import override_settings
from dms.tests.base import MongoTestCase
from dms.utils.rapidpro_message_utils import split_text


class RapidProMessageUtilsTest(MongoTestCase):

    @override_settings(MESSAGE_MILITARY_SEPARATOR='*')
    def test_text_messages_are_split_and_white_space_removed(self):
        text_message = "NECOC* Kampala * Central Division*            Fire"
        self.assertEqual(["NECOC", "Kampala", "Central Division", "Fire"], split_text(text_message))
