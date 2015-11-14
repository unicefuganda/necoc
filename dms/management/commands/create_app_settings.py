from django.core.management import BaseCommand
from mongoengine.django.auth import Permission, Group
from dms.models import  AdminSetting, User


class Command(BaseCommand):
    args = './manage.py create_app_settings <setting_name> <yes_no> <value_str> <value_int>'
    help = 'Creates an app setting with a default value ( setting_name_must_be_under_scored )'

    def handle(self, *args, **options):
        if not len(args):
            # AdminSetting.objects(**dict(name='enable_automatic_response')).first() or \
            #                    AdminSetting(**dict(name='enable_automatic_response')).save()
            #
            # AdminSetting.objects(**dict(name='send_this_number_of_automatic_responses_then_stop', value_int=10)).first() or \
            #               AdminSetting(**dict(name='send_this_number_of_automatic_responses_then_stop', value_int=10)).save()

            #Attach ability to manage these settings to admin user by default
            # (This is hack since mongo engine Permissions is broken
            # admin_user = User.objects(**dict(username='admin')).first()
            # ct_id = admin_user.group.permissions[0].content_type
            # manage_settings = Permission(name='can manage settings', codename='can_manage_settings', content_type=ct_id).save()

            # if not manage_settings in admin_user.group.permissions:
            #     user_group = admin_user.group
            #     group_permissions = user_group.permissions
            #     new_permissions = group_permissions.append(manage_settings)
            #     user_group.permissions = new_permissions
            #     user_group.save()
            all_permissions = Permission.objects.all()
            g = Group.objects.get(name='Administrator')
            g.permissions = all_permissions
            g.save()
        else:
            if len(args) is 4:
                if AdminSetting.objects(**dict(name='enable_automatic_response')).first():
                    setting = AdminSetting.objects(**dict(name='enable_automatic_response')).first()
                    setting.yes_no = args[1]
                    setting.value_str = args[2]
                    setting.value_int = args[3]
                    setting.save()
                else:
                    AdminSetting.objects(**dict(name=args[0], yes_no=args[1], value_str=args[2], value_int=args[3])).save()
            else:
                self.stdout.write('Expects 0 or 4 arguments in format: <setting_name> <yes_no> <value_str> <value_int>!')
        self.stdout.write('Settings Added!')