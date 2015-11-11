from django.core.management import BaseCommand
from dms.models import  AdminSetting


class Command(BaseCommand):
    args = './manage.py create_app_settings <setting_name> <yes_no> <value_str> <value_int>'
    help = 'Creates an app setting with a default value ( setting_name_must_be_under_scored )'

    def handle(self, *args, **options):
        if not len(args):
            AdminSetting.objects(**dict(name='enable_automatic_response')).first() or \
                               AdminSetting(**dict(name='enable_automatic_response')).save()

            AdminSetting.objects(**dict(name='send_this_number_of_automatic_responses_then_stop', value_int=10)).first() or \
                          AdminSetting(**dict(name='send_this_number_of_automatic_responses_then_stop', value_int=10)).save()
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