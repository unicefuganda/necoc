from rest_framework import fields
from rest_framework.response import Response
from dms.api.retrieve_update_wrapper import MongoRetrieveUpdateView
from dms.models.admin_setting import AdminSetting
from rest_condition import Or
from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.generics import ListCreateAPIView, ListAPIView
from dms.utils.permission_class_factory import build_permission_class, IsGetRequest


__author__ = 'asseym'


class AdminSettingSerializer(serializers.MongoEngineModelSerializer):
    name = fields.CharField(source='name')
    yes_no = fields.BooleanField(source='yes_no', default=True)
    value_str = fields.CharField(source='value_str', required=False)
    value_int = fields.IntegerField(source='value_int', required=False)

    class Meta:
        model = AdminSetting
        fields = ('name', 'yes_no', 'value_str', 'value_int')


class AdminSettingListCreateView(ListCreateAPIView):
    model = AdminSetting
    serializer_class = AdminSettingSerializer
    queryset = AdminSetting.objects()
    permission_classes = [Or(build_permission_class('dms.can_manage_settings'), IsGetRequest)]
    lookup_field = 'name'


class AdminSettingUpdateView(MongoRetrieveUpdateView):
    serializer_class = AdminSettingSerializer
    queryset = AdminSetting.objects.all()
    permission_classes = [Or(build_permission_class('dms.can_manage_settings'), IsGetRequest)]
    lookup_field = 'name'

    def list(self, request, *args, **kwargs):
        setting = AdminSetting.objects(name=kwargs['name']).first()
        serializer = AdminSettingSerializer(setting)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
