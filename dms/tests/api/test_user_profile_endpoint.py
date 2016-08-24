from collections import OrderedDict
import collections
import json
from django.conf import settings
from django.test import override_settings
import mock
from mongoengine.django.auth import Group
import time
from rest_framework_csv.renderers import CSVRenderer
from dms.models import User, Location, UserProfile
from dms.tests.base import MongoAPITestCase
from dms.utils.rapidpro_message_utils import split_text


class FakeImageResizer:
    def __init__(self, image):
        self.image = image

    def generate(self):
        return self.image


class BadImageResizer:
    def __init__(self, image):
        raise Exception('Something has gone wrong')


def dict_replace(param, replace, datadict):
    for key, value in datadict.items():
        if key == param:
            datadict[key] = replace
    return datadict


class TestUserProfileEndpoint(MongoAPITestCase):
    API_ENDPOINT = '/api/v1/mobile-users/'
    CSV_ENDPOINT = '/api/v1/csv-mobile-users/'
    BULK_ENDPOINT = '/api/v1/bulk-mobile-users/'

    def setUp(self):
        self.login_user()
        self.district = Location(**dict(name='Kampala', type='district', parent=None))
        self.district.save()
        self.masaka = Location(**dict(name='Masaka', type='district', parent=None)).save()
        self.subcounty = Location(**dict(name='Nangabo', type='subcounty', parent=self.masaka)).save()

        self.mobile_user_to_post = dict(name='tim', phone='+256775019500', location=self.district.id,
                                        email='tim@akampa.com')
        self.mobile_user = dict(name='timothy', phone='+256775019449', location=self.district, email=None)
        self.masaka_user = dict(name='Munamasaka', phone='+256775019441', location=self.subcounty, email='m@emasaka.com')

    def tearDown(self):
        UserProfile.drop_collection()

    def test_should_post_a_mobile_user(self):
        response = self.client.post(self.API_ENDPOINT, data=self.mobile_user_to_post)
        self.assertEqual(201, response.status_code)

        retrieved_user = UserProfile.objects(name='tim')
        self.assertEqual(1, retrieved_user.count())

    def test_should_get_a_list_of_users(self):
        user_profile = UserProfile(**self.mobile_user).save()
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(self.mobile_user['name'], response.data[0]['name'])
        self.assertEqual(self.mobile_user['phone'], response.data[0]['phone'])
        self.assertEqual(self.mobile_user['email'], response.data[0]['email'])
        self.assertEqual(user_profile.username(), '')
        self.assertEqual(self.district.name, response.data[0]['location']['name'])

    def test_should_get_ordered_list_of_users(self):
        mob_users = [('aa', '+256775019441'), ('zz', '+256775019442'), ('tim', '+256775019443'), ('abu' , '+256775019444')]
        for user_name, mob in mob_users:
            new_dict = dict_replace('name', user_name, self.mobile_user)
            new_dict = dict_replace('phone', mob, new_dict)
            UserProfile(**new_dict).save()
            time.sleep(1)
        response = self.client.get(self.API_ENDPOINT, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(mob_users), len(response.data))
        self.assertEqual(response.data[0]['name'], 'abu')
        self.assertEqual(response.data[3]['name'], 'aa')

        #post order by name
        response = self.client.get(self.API_ENDPOINT + '?ordering=name', format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data[0]['name'], 'aa')
        self.assertEqual(response.data[1]['name'], 'abu')
        self.assertEqual(response.data[2]['name'], 'tim')
        self.assertEqual(response.data[3]['name'], 'zz')

        #post order by name desc
        response = self.client.get(self.API_ENDPOINT + '?ordering=-name', format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.data[0]['name'], 'zz')
        self.assertEqual(response.data[1]['name'], 'tim')
        self.assertEqual(response.data[2]['name'], 'abu')
        self.assertEqual(response.data[3]['name'], 'aa')



    def test_raise_403_if_user_doesnt_have_manage_permission(self):
        self.assert_permission_required_for_get(self.API_ENDPOINT)
        self.assert_permission_required_for_post(self.API_ENDPOINT)

    def test_should_get_a_single_user(self):
        attr = self.mobile_user.copy()
        user = User(username='cage', password='haha').save()
        attr['user'] = user
        profile = UserProfile(**attr).save()

        response = self.client.get(self.API_ENDPOINT + str(profile.id) + '/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.mobile_user['name'], response.data['name'])
        self.assertEqual(self.mobile_user['phone'], response.data['phone'])
        self.assertEqual(self.mobile_user['email'], response.data['email'])
        self.assertEqual(self.district.name, response.data['location']['name'])
        self.assertEqual('cage', response.data['username'])
        self.assertEqual(str(user.id), response.data['user_id'])


    def test_should_update_a_single_user(self):
        attr = self.mobile_user.copy()
        attr['email'] = 'tim@akampa.com'
        attr['phone'] = '+256775019500'
        attr['user'] = User(username='cage', password='haha').save()
        profile = UserProfile(**attr).save()
        response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/', self.mobile_user_to_post)

        profile.reload()
        profiles = UserProfile.objects()
        self.assertEqual(1, profiles.count())

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.mobile_user_to_post['name'], profile.name)
        self.assertEqual(self.mobile_user_to_post['phone'], profile.phone)
        self.assertEqual(self.mobile_user_to_post['email'], profile.email)

    def test_raise_403_given_user_is_trying_to_access_some_other_users_profile(self):
        attr = self.mobile_user.copy()
        attr['email'] = 'someother@email.com'
        attr['phone'] = '+256775029500'
        attr['user'] = User(username='someother', password='hahahah').save()
        profile = UserProfile(**attr).save()
        self.assert_permission_required_for_get(self.API_ENDPOINT + str(profile.id) + '/')
        self.assert_permission_required_for_post(self.API_ENDPOINT + str(profile.id) + '/')

    def test_not_raising_403_if_user_only_wants_access_to_their_profile(self):
        self.client.logout()
        attr = self.mobile_user.copy()
        attr['email'] = 'someother@email.com'
        attr['phone'] = '+256775029500'
        user = User(username='someother11', email='hahahaha@hahahahaha.ha')
        user.group = None
        user.set_password('hahahah')
        attr['user'] = user
        profile = UserProfile(**attr).save()
        self.client.login(username='someother11', password='hahahah')

        response = self.client.get(self.API_ENDPOINT + str(profile.id) + '/')
        self.assertEquals(response.status_code, 200)
        response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/')
        self.assertEquals(response.status_code, 200)

    def test_post_with_non_empty_username_creates_system_user(self):
        attr = self.mobile_user_to_post.copy()
        attr['username'] = 'akampa'
        response = self.client.post(self.API_ENDPOINT, data=attr)
        self.assertEqual(201, response.status_code)

        retrieved_user_profile = UserProfile.objects(name='tim')
        self.assertEqual(1, retrieved_user_profile.count())

        retrieved_user = User.objects(username='akampa')
        self.assertEqual(1, retrieved_user.count())
        self.assertEqual(retrieved_user.first(), retrieved_user_profile.first().user)

    @mock.patch('dms.tasks.send_email.delay')
    def test_posting_new_system_user_sends_email(self, mock_send_email):
        attr = self.mobile_user_to_post.copy()
        attr['username'] = 'akampa'
        attr['email'] = 'email@email.email'
        response = self.client.post(self.API_ENDPOINT, data=attr)
        self.assertEqual(201, response.status_code)
        mock_send_email.assert_called_with('Your NECOC Account',
                                           mock.ANY,
                                           settings.DEFAULT_FROM_EMAIL,
                                           ['email@email.email'])

    def test_post_with_group_associates_user_to_group(self):
        attr = self.mobile_user_to_post.copy()
        attr['username'] = 'akampa'
        group = Group.objects().first()
        attr['group'] = str(group.id)
        response = self.client.post(self.API_ENDPOINT, data=attr)
        self.assertEqual(201, response.status_code)

        retrieved_user = User.objects(username='akampa').first()
        self.assertEqual(group, retrieved_user.group)

    def test_update_with_group_associates_user_to_new_group(self):
        attr = self.mobile_user_to_post.copy()
        attr['username'] = 'akampa'
        group = Group.objects().first()
        attr['group'] = str(group.id)
        self.client.post(self.API_ENDPOINT, data=attr)

        retrieved_user = User.objects(username='akampa').first()
        retrieved_user_profile = UserProfile.objects(user=retrieved_user).first()
        new_group = Group.objects().all()[2]

        new_attr = self.mobile_user_to_post.copy()
        new_attr['username'] = 'akampa'
        new_attr['location'] = str(new_attr['location'])
        new_attr['group'] = str(new_group.id)
        new_attr['id'] = str(retrieved_user_profile.id)

        url = self.API_ENDPOINT + str(retrieved_user_profile.id) + '/'
        response = self.client.post(url,
                                    data=new_attr)
        self.assertEqual(200, response.status_code)
        retrieved_user = User.objects(username='akampa').first()
        self.assertEqual(new_group, retrieved_user.group)

    @mock.patch('dms.utils.image_resizer.ImageResizer', FakeImageResizer)
    def test_post_with_photo_file(self):
        attr = self.mobile_user_to_post.copy()
        attr['username'] = 'akampa'

        with open(settings.PROJECT_ROOT + '/../dms/tests/test.jpg', 'rb') as test_image:
            attr['file'] = test_image
            response = self.client.post(self.API_ENDPOINT, data=attr)

        self.assertEqual(201, response.status_code)

        retrieved_user = User.objects(username='akampa').first()
        reloaded_profile = UserProfile.objects(user=retrieved_user).first()
        self.assertEqual(reloaded_profile.photo.read(),
                         open(settings.PROJECT_ROOT + '/../dms/tests/test.jpg', 'rb').read())
        self.assertEqual(reloaded_profile.photo.content_type, 'image/jpeg')
        self.assertEqual(reloaded_profile.photo_uri(), '/api/v1/photo/' + str(reloaded_profile.id))

    @mock.patch('dms.utils.image_resizer.ImageResizer', BadImageResizer)
    def test_post_with_photo_file(self):
        attr = self.mobile_user_to_post.copy()
        attr['username'] = 'akampa'

        with open(settings.PROJECT_ROOT + '/../dms/tests/test.jpg', 'rb') as test_image:
            attr['file'] = test_image
            response = self.client.post(self.API_ENDPOINT, data=attr)

        self.assertEqual(201, response.status_code)

        retrieved_user = User.objects(username='akampa').first()
        reloaded_profile = UserProfile.objects(user=retrieved_user).first()
        self.assertEqual(reloaded_profile.photo.read(), None)

    @mock.patch('dms.utils.image_resizer.ImageResizer', FakeImageResizer)
    def test_updating_profile_with_photo_file(self):
        attr = self.mobile_user_to_post.copy()
        attr['email'] = 'tim@akampa.com'
        attr['phone'] = '+256775019511'
        attr['user'] = User(username='cage2', password='haha').save()
        profile = UserProfile(**attr)
        user_photo = open(settings.PROJECT_ROOT + '/../dms/tests/test.jpg', 'rb')
        profile.photo.put(user_photo, content_type='image/content_type')
        profile.save()

        with open(settings.PROJECT_ROOT + '/../dms/tests/test2.jpg', 'rb') as test_image:
            attr['file'] = test_image
            response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/', attr)
            self.assertEqual(200, response.status_code)

        retrieved_user = User.objects(username='cage2').first()
        reloaded_profile = UserProfile.objects(user=retrieved_user).first()
        self.assertEqual(reloaded_profile.photo.read(),
                         open(settings.PROJECT_ROOT + '/../dms/tests/test2.jpg', 'rb').read())
        self.assertEqual(reloaded_profile.photo.content_type, 'image/jpeg')
        self.assertEqual(reloaded_profile.photo_uri(), '/api/v1/photo/' + str(reloaded_profile.id))

    @mock.patch('dms.utils.image_resizer.ImageResizer', BadImageResizer)
    def test_handling_photo_update_exception(self):
        attr = self.mobile_user_to_post.copy()
        attr['email'] = 'tim@akampa.com'
        attr['phone'] = '+256775019511'
        attr['user'] = User(username='cage2', password='haha').save()
        profile = UserProfile(**attr)
        user_photo = open(settings.PROJECT_ROOT + '/../dms/tests/test.jpg', 'rb')
        profile.photo.put(user_photo, content_type='image/content_type')
        profile.save()

        with open(settings.PROJECT_ROOT + '/../dms/tests/test2.jpg', 'rb') as test_image:
            attr['file'] = test_image
            response = self.client.post(self.API_ENDPOINT + str(profile.id) + '/', attr)
            self.assertEqual(200, response.status_code)

        retrieved_user = User.objects(username='cage2').first()
        reloaded_profile = UserProfile.objects(user=retrieved_user).first()
        self.assertEqual(reloaded_profile.photo.read(), None)

    def test_should_return_csv_when_csv_endpoint_is_called(self):
        self.mobile_user['email'] = 'mobile_user@mobuser.com'
        UserProfile(**self.mobile_user).save()
        UserProfile(**self.masaka_user).save()
        response = self.client.get(self.CSV_ENDPOINT, format='csv')

        expected_response = "name,phone,email,district,subcounty\r\n" \
                            "timothy,+256775019449,mobile_user@mobuser.com,%s,%s" % (self.district.name,'')
        expected_response = expected_response + "\r\nMunamasaka,+256775019441,m@emasaka.com,%s,%s" % (self.masaka.name, self.subcounty.name)

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

    def test_should_return_csv_with_all_users_when_location_is_empty_when_csv_endpoint_is_called(self):
        self.mobile_user['email'] = 'mobile_user@mobuser.com'
        UserProfile(**self.mobile_user).save()
        UserProfile(**self.masaka_user).save()
        response = self.client.get(self.CSV_ENDPOINT + '?location=', format='csv')

        expected_response = "name,phone,email,district,subcounty\r\n" \
                            "timothy,+256775019449,mobile_user@mobuser.com,%s,%s" % (self.district.name,'')
        expected_response = expected_response + "\r\nMunamasaka,+256775019441,m@emasaka.com,%s,%s" % (self.masaka.name, self.subcounty.name)

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))
        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

    def test_should_return_filtered_csv_when_csv_endpoint_is_called_with_location_filter(self):
        self.mobile_user['email'] = 'mobile_user@mobuser.com'
        UserProfile(**self.mobile_user).save()
        UserProfile(**self.masaka_user).save()
        response = self.client.get(self.CSV_ENDPOINT + '?location=%s' % self.masaka.id, format='csv')

        expected_response = "name,phone,email,district,subcounty\r\n" \
                            "Munamasaka,+256775019441,m@emasaka.com,%s,%s" % (self.masaka.name, self.subcounty.name)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertTrue(isinstance(response.accepted_renderer, CSVRenderer))
        result_set = set(split_text(expected_response)) & set(split_text(response.content))
        self.assertEqual(collections.Counter(split_text(expected_response)), collections.Counter(split_text(response.content)))

    def test_should_bulk_save_streamed_csv_user_profiles(self):
        dup_user = self.masaka_user.copy()
        dup_user['name'] = 'AnotherMasakarian'
        UserProfile(**dup_user).save()
        self.assertEqual(dup_user['name'], UserProfile.objects(**dup_user).first().name)
        dup_user['name'] = 'NamedChanged'
        bulk_mobile_users = [
            {
                "name":"%s" % self.masaka_user['name'],
                "phone":"%s" % self.masaka_user['phone'],
                "email": "%s" % self.masaka_user['email'],
                "district": "%s" % self.masaka.name,
                "subcounty": "%s" % self.subcounty.name,
             },
            {
                "name":"%s" % self.mobile_user['name'],
                "phone":"%s" % self.mobile_user['phone'],
                "email": None,
                "district": "%s" % self.district.name,
                "subcounty": "%s" % '',
             },
            {
                "name":"%s" % dup_user['name'],
                "phone":"%s" % dup_user['phone'],
                "email": "%s" % dup_user['email'],
                "district": "%s" % self.masaka.name,
                "subcounty": "%s" % self.subcounty.name,
             },
        ]

        response = self.client.post(self.BULK_ENDPOINT, bulk_mobile_users, format='json')

        self.assertEqual(2, UserProfile.objects.count())
        response = UserProfile.objects(**self.masaka_user)
        self.assertEqual(0, response.count())
        response = UserProfile.objects(**dup_user)
        self.assertEqual(1, response.count())
        self.assertEqual(dup_user['name'], UserProfile.objects(**dup_user).first().name)
        self.mobile_user['email']="" #empty string is not equal to None
        response = UserProfile.objects(**self.mobile_user)
        self.assertEqual(1, response.count())

    def test_should_omit_invalid_csv_rows_but_save_valid_ones(self):

        bulk_mobile_users = [
            {
                "name":"new name",
                "phone":"+256771289018",
                "email": "me@me.com",
                "district": "%s" % self.masaka.name,
                "subcounty": "unknownSub", #unknown subcounty
             },
            {
                "name":"new name",
                "phone":"+256771289018",
                "email": "me@me.com",
                "district": "unknowndistrict", #unknown district
                "subcounty": None,
             },
            {
                "name":"new name",
                "phone":"+256771289018",
                "email": "me@me.com",
                "district": "unknowndistrict", #unknown district
                "subcounty": "badsubcounty", #unknown subcounty
             },
            {
                "name":"%s" % self.mobile_user['name'],
                "phone":"%s" % self.mobile_user['phone'],
                "email": None,
                "district": "%s" % self.district.name,
                "subcounty": "%s" % '',
             },
        ]

        response = self.client.post(self.BULK_ENDPOINT, bulk_mobile_users, format='json')

        self.assertEqual(1, UserProfile.objects.count())
        masaka_users = UserProfile.objects(name=self.masaka_user['name'])
        self.assertEqual(0, masaka_users.count())
        self.mobile_user['email']="" #empty string is not equal to None
        kampala_users = UserProfile.objects(**self.mobile_user)
        self.assertEqual(1, kampala_users.count())

    def test_should_omit_empty_csv_rows(self):

        bulk_mobile_users = [
            {
                "name":"new name",
                "phone":"+256771289018",
                "email": "me@me.com",
                "district": "%s" % self.masaka.name,
                "subcounty": "unknownSub",
             },
            {},
            {
                "name":"%s" % self.mobile_user['name'],
                "phone":"%s" % self.mobile_user['phone'],
                "email": None,
                "district": "%s" % self.district.name,
                "subcounty": "%s" % '',
             },
        ]

        response = self.client.post(self.BULK_ENDPOINT, bulk_mobile_users, format='json')

        self.assertEqual(1, UserProfile.objects.count())
        masaka_users = UserProfile.objects(name=self.masaka_user['name'])
        self.assertEqual(0, masaka_users.count())
        self.mobile_user['email']="" #empty string is not equal to None
        kampala_users = UserProfile.objects(**self.mobile_user)
        self.assertEqual(1, kampala_users.count())

    def test_should_omit_blank_csv(self):

        bulk_mobile_users = [
            {},
        ]

        response = self.client.post(self.BULK_ENDPOINT, bulk_mobile_users, format='json')
        self.assertEqual(0, UserProfile.objects.count())

