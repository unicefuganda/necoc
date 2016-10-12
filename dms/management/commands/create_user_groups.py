from django.core.management import BaseCommand
from mongoengine.django.auth import Group, ContentType, Permission


class Command(BaseCommand):
    args = './manage.py create_user_groups'
    help = 'Creates user groups fixtures'

    def handle(self, *args, **options):
        try:
            # ct, created = ContentType.objects.get_or_create(app_label='dms', model='', name='')
            ct = ContentType(app_label='dms', model='', name='').save()
            manage_users = Permission(name='can manage users', codename='can_manage_users', content_type=ct.id).save()
            manage_polls = Permission(name='can manage polls', codename='can_manage_polls', content_type=ct.id).save()
            view_polls = Permission(name='can view polls', codename='can_view_polls', content_type=ct.id).save()
            view_messages = Permission(name='can view messages', codename='can_view_messages', content_type=ct.id).save()
            view_disasters = Permission(name='can view disasters', codename='can_view_disasters', content_type=ct.id).save()
            manage_disasters = Permission(name='can manage disasters', codename='can_manage_disasters',
                                          content_type=ct.id).save()
            manage_messages = Permission(name='can manage messages', codename='can_manage_messages',
                                         content_type=ct.id).save()
            manage_settings = Permission(name='can manage settings', codename='can_manage_settings', content_type=ct.id).save()

            Group(name='Administrator', permissions=[manage_users,
                                                     manage_polls,
                                                     view_polls,
                                                     view_disasters,
                                                     manage_disasters,
                                                     manage_messages,
                                                     manage_settings,]).save()

            Group(name='IT Assistant', permissions=[view_polls,
                                                    view_disasters,
                                                    manage_disasters,
                                                    manage_messages]).save()

            Group(name='Disaster Preparedness Officer', permissions=[manage_polls,
                                                                     view_polls,
                                                                     manage_disasters,
                                                                     manage_messages]).save()

            Group(name='Disaster Management Officer', permissions=[manage_polls,
                                                                   view_polls,
                                                                   view_disasters,
                                                                   manage_disasters,
                                                                   manage_messages]).save()

            Group(name='Management Team', permissions=[manage_users,
                                                       manage_polls,
                                                       view_polls,
                                                       manage_disasters,
                                                       manage_messages]).save()

            Group(name='DDMC Chairperson', permissions=[view_polls,
                                                        view_messages,
                                                        view_disasters]).save()

            Group(name='CAO', permissions=[view_polls,
                                           view_messages,
                                           view_disasters]).save()

            Group(name='DDMC', permissions=[view_polls,
                                           view_messages,
                                           view_disasters]).save()
        except:
            print "You have likely created the user group data already"