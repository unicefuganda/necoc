from django.core.management import BaseCommand
from mongoengine.django.auth import Group
from dms.models import UserProfile, Location, User


class Command(BaseCommand):
    args = './manage.py create_super_user <username> <password> <email> <name> <location> <phone>'
    help = 'Creates a super user with credentials that you pass in'

    def handle(self, *args, **options):
        if not len(args):
            user = User.objects(username='admin').first() or User(username='admin').save()
            user.group = Group.objects(name='Administrator').first()
            user.set_password('password')
            location = Location.objects(type='district').first() or Location(name='Kampala', type='district').save()
            profile = UserProfile.objects(phone='N/A').first() or UserProfile(phone='N/A', name='Admin', location=location, email='admin@admin.admin').save()
            profile.user = user
            profile.save()
        else:
            user = User.objects(username=args[0]).first() or User(username=args[0]).save()
            user.group = Group.objects(name='Administrator').first()
            user.set_password(args[1])
            location = Location.objects(name=args[4]).first() or Location(name=args[4], type='district').save()
            profile = UserProfile.objects(phone=args[5]).first() or UserProfile(phone=args[5], name=args[3], location=location, email=args[2]).save().save()
            profile.user = user
            profile.save()

        self.stdout.write('Successfully created superuser')