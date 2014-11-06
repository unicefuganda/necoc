from django.core.management import BaseCommand
from mongoengine.django.auth import User
from dms.models import UserProfile, Location


class Command(BaseCommand):
    args = './manage.py create_super_user <username> <password> <email> <name> <location> <phone>'
    help = 'Creates a super user with credentials that you pass in'

    def handle(self, *args, **options):
        if not len(args):
            user = User(username='admin').save()
            user.set_password('password')
            location = Location.objects(type='district').first() or Location(name='Kampala', type='district').save()
            UserProfile(phone='N/A', name='Admin', location=location, user=user, email='admin@admin.admin').save()
        else:
            user = User(username=args[0]).save()
            user.set_password(args[1])
            location = Location.objects(name=args[4]).first()
            UserProfile(phone=args[5], name=args[3], location=location, user=user, email=args[2]).save()

        self.stdout.write('Successfully created superuser')