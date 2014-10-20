from dms.tests.base import MongoTestCase
from dms.utils.rapidpro_message_utils import split_text


class RapidProMessageUtilsTest(MongoTestCase):

    def test_text_messages_are_split_and_white_space_removed(self):
        text_message = "NECOC  Kampala            Fire"
        self.assertEqual(["NECOC", "Kampala", "Fire"], split_text(text_message))
