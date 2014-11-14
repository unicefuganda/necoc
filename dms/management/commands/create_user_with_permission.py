import random
import uuid
from django.core.management import BaseCommand
from mongoengine.django.auth import Group, Permission, ContentType
from dms.models import UserProfile, Location, User


class Command(BaseCommand):
    args = './manage.py create_super_user <username> <password> <email> <permission>'
    help = 'Creates a user with credentials that you pass in'

    def handle(self, *args, **options):
        if len(args):
            user = User.objects(username=args[0], email=args[2]).first() or User(username=args[0], email=args[2])
            if len(args) > 3:
                ct = ContentType(app_label='dms', model=str(uuid.uuid4()), name=str(uuid.uuid4())).save()
                permission = Permission(name=args[3], codename=args[3], content_type=ct.id).save()
                group = Group(name=str(uuid.uuid4()), permissions=[permission]).save()
                user.group = group

            user.set_password(args[1])

            self.stdout.write('Successfully created user')