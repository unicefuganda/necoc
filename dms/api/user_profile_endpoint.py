import json
from mongoengine import NotUniqueError, ValidationError, DoesNotExist
from mongoengine.django.auth import Group
from rest_condition import Or
from rest_framework.permissions import BasePermission
from rest_framework.settings import api_settings
from rest_framework_bulk import BulkSerializerMixin, ListBulkCreateUpdateDestroyAPIView, ListBulkCreateAPIView, \
    BulkCreateModelMixin
from rest_framework_csv.parsers import CSVParser
from rest_framework_csv.renderers import CSVRenderer
from rest_framework_mongoengine.generics import ListCreateAPIView
from rest_framework_mongoengine import serializers
from rest_framework import serializers as rest_serializers
from rest_framework import fields
from rest_framework.response import Response
from rest_framework import status
from dms.models import User, Location
from dms.api.retrieve_update_wrapper import MongoRetrieveUpdateView
from dms.models.user_profile import UserProfile
from dms.services.user_profile_service import UserProfileService
from dms.utils import image_resizer
from dms.utils.permission_class_factory import build_permission_class
from dms.utils.user_profile_utils import get_profile


class UserProfileSerializer(serializers.MongoEngineModelSerializer):
    username = fields.CharField(source='username', required=False)
    user_id = fields.CharField(source='user_id', required=False)
    group = fields.CharField(source='group', required=False)
    group_name = fields.CharField(source='group_name', required=False, read_only=True)
    photo_uri = fields.CharField(source='photo_uri', required=False)

    def validate_phone(self, attrs, source):
        phone = attrs.get(source)
        updated_value = phone != getattr(self.object, 'phone', '')
        self.__check_uniqueness(attrs, 'phone', UserProfile.objects(phone=phone), updated_value)
        return attrs

    def validate_email(self, attrs, source):
        email = attrs.get(source)
        updated_value = email != getattr(self.object, 'email', '')
        if not email:
            return attrs
        self.__check_uniqueness(attrs, 'email', UserProfile.objects(email=email), updated_value)
        return attrs

    def validate_username(self, attrs, source):
        username = attrs.get(source)
        updated_value = not (self.object and username == self.object.username())
        self.__check_uniqueness(attrs, 'username', User.objects(username=username), updated_value)
        return attrs

    def __check_uniqueness(self, attrs, field, objects_with_same_field_value, updated_value):
        if objects_with_same_field_value and updated_value:
            is_new_record = not attrs.get('id')
            has_non_unique_field_value = attrs.get('id') != objects_with_same_field_value.first().id
            if is_new_record or has_non_unique_field_value:
                raise rest_serializers.ValidationError(field.capitalize() + ' must be unique')

    class Meta:
        model = UserProfile
        exclude = ('created_at', 'user', 'photo')


class UserProfileListCreateView(ListCreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects()
    model = UserProfile
    permission_classes = (build_permission_class('dms.can_manage_users'),)

    def get_queryset(self):
        query_params = {key: value or None for key, value in self.request.GET.items()}
        if 'ordering' in query_params:
            ordering_params = query_params['ordering']
            del query_params['ordering']
            query_set = UserProfile.objects(**query_params).order_by('%s' % ordering_params)
        else:
            query_set = UserProfile.objects(**query_params).order_by('-created_at')
        return query_set

    def pre_save(self, obj):
        username = self.request.DATA.get('username', None)
        group_id = self.request.DATA.get('group', None)
        if username:
            user = UserProfileService(obj).setup_new_user(username, group_id)
            obj.user = user

    def save_new_image(self, obj):
        try:
            if self.request.FILES.get('file'):
                image = image_resizer.ImageResizer(self.request.FILES.get('file')).generate().read()
                content_type = self.request.FILES.get('file').content_type
                obj.photo.put(image, content_type=content_type)
                obj.save()
        except:
            obj.photo.delete()
            obj.save()

    def post_save(self, obj, created=False):
        self.save_new_image(obj)


class CSVUserProfileSerializer(serializers.MongoEngineModelSerializer):
    name = fields.CharField(source='name', required=False)
    phone = fields.CharField(source='phone', required=False)
    email = fields.CharField(source='email', required=False)
    district = fields.CharField(source='district', required=False)
    subcounty = fields.CharField(source='subcounty', required=False)

    class Meta:
        model = UserProfile
        exclude = ('created_at', 'user', 'photo', 'photo_uri', 'username', 'user_id', 'group', 'group_name', 'location', 'id')


class CSVUserProfileView(ListCreateAPIView):
    serializer_class = CSVUserProfileSerializer
    permission_classes = (build_permission_class('dms.can_manage_users'),)
    model = UserProfile
    renderer_classes = [CSVRenderer, ] + api_settings.DEFAULT_RENDERER_CLASSES
    parser_classes = (CSVParser,)

    def get_queryset(self):
        params = self._filter_params(self.request)
        queryset = UserProfile.objects.filter(**params)
        return queryset.order_by('-created_at')

    def _filter_params(self, req):
        location = req.GET.get('location')
        params = {}
        locations = []
        if location and not self._undefined(location):
            locs = location.split(',')
            for loc in locs:
                locations += Location.objects(**dict(id=loc)).first().children(include_self=True)
            params = {'location__in': locations}
        return params

    def _undefined(self, strValue):
        return strValue == u'undefined'


class BulkUserProfileSerializer(BulkSerializerMixin, serializers.MongoEngineModelSerializer):
    name = fields.CharField(source='name', required=True)
    phone = fields.CharField(source='phone', required=True)
    email = fields.CharField(source='email', required=False)
    location = fields.Field(source='location')

    class Meta(object):
        model = UserProfile
        exclude = ('created_at',)


class BulkUserProfileView(ListBulkCreateUpdateDestroyAPIView):
    serializer_class = BulkUserProfileSerializer
    permission_classes = (build_permission_class('dms.can_manage_users'),)
    model = UserProfile

    def get_queryset(self):
        return UserProfile.objects()

    def post(self, request, *args, **kwargs):
        request = self._prep_request(request)
        return self.create(request, *args, **kwargs) if len(request.DATA) else Response('Invalid CSV')

    def create(self, request, *args, **kwargs):
        bulk = isinstance(request.DATA, list)
        midx = len(request.DATA)-1

        if not bulk:
            return super(BulkCreateModelMixin, self).create(request, *args, **kwargs)

        else:
            serializer = self.get_serializer(data=request.DATA, many=True)
            if serializer.is_valid():
                objects = []
                data_list = request.DATA

                for obj in serializer.object:
                    self.pre_save(obj)
                for i, d in enumerate(data_list):
                    request.DATA = data_list[i:i+1] if i<midx else [data_list[midx]]
                    try:
                        resp = super(BulkUserProfileView, self).create(request, *args, **kwargs)
                        if resp.status_code == status.HTTP_201_CREATED:
                            objects.append(resp)
                    except NotUniqueError:
                        profile = get_profile(request.DATA[0]['phone'])
                        request.DATA[0]['id'] = '%s' % profile.id
                        resp = self.patch(request, *args, **kwargs)
                        if resp.status_code == status.HTTP_200_OK:
                            objects.append(resp)

                self.object = objects
                for obj in self.object:
                    self.post_save(obj, created=True) if obj.status_code==status.HTTP_201_CREATED else \
                    self.post_save(obj, created=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def _prep_request(self, request):
        request._request.DATA = request.DATA
        request = request._request #drf 2.2.* requests are imutable, use the mutable django request
        request = self._insert_location(request)
        request = self._remove_bad_locations(request)
        return request

    def _insert_location(self, request):
        data = request.DATA
        params = {}
        for i, dt in enumerate(data):
            sub_name = dt.get('subcounty', None)
            dist_name = dt.get('district', None)
            try:
                if sub_name and dist_name:
                    parent = Location.objects(name=dist_name, type='district').first()
                    params = dict(name=sub_name, type='subcounty', parent=parent)
                    self.discard_loc_aliases(request.DATA[i])
                elif dist_name:
                    params = dict(name=dist_name, type='district')
                    self.discard_loc_aliases(request.DATA[i])
                elif sub_name:
                    params = dict(name=sub_name, type='subcounty')
                    self.discard_loc_aliases(request.DATA[i])
                else:
                    # print 'no district and subcounty specified for record: %s' % request.DATA[i]
                    continue
                request.DATA[i]['location'] = Location.objects.get(**params)
            except Exception as e:
                # print '%s: something wrong with district name [%s] or subcounty name [%s] \
                # specified for record' % (e.__class__.__name__, dist_name, sub_name)
                continue
        return request

    def _remove_bad_locations(self, request):
        for i, d in enumerate(request.DATA):
            if not 'location' in d.keys():
                request.DATA[i] = {}
        request.DATA = filter(None, request.DATA) #remove empty dicts
        return request

    def discard_loc_aliases(self, loc):
        del loc['district']
        del loc['subcounty']


class IsCurrentUsersProfile(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous():
            return False
        user_id = str(UserProfile.objects.get(user=request.user).id)
        return user_id in request.path


class UserProfileView(MongoRetrieveUpdateView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [Or(build_permission_class('dms.can_manage_users'), IsCurrentUsersProfile), ]

    def list(self, request, *args, **kwargs):
        user_profile = UserProfile.objects(id=kwargs['id']).first()
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def replace_image(self, obj):
        try:
            if self.request.FILES.get('file'):
                image = image_resizer.ImageResizer(self.request.FILES.get('file')).generate().read()
                content_type = self.request.FILES.get('file').content_type
                obj.photo.replace(image, content_type=content_type)
                obj.save()
        except:
            obj.photo.delete()
            obj.save()

    def post_save(self, obj, created=False):
        group_id = self.request.DATA.get('group', None)
        if(group_id):
            obj.user.group = Group.objects(id=group_id).first()
            obj.user.save()
        self.replace_image(obj)