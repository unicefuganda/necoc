from dms.models import Location, UserProfile, User
from dms.templatetags.generic_tags import get_profile_id
from dms.tests.base import MongoTestCase


class TemplateTagsTest(MongoTestCase):
    def test_mapping_user_id_to_user_profile(self):
        user = User(username='admin').save()
        location = Location(name='Kampala', type='district').save()

        profile = UserProfile(phone='N/A', name='Admin', location=location, user=user, email='admin@admin.admin').save()

        self.assertEqual(profile.id, get_profile_id(user))