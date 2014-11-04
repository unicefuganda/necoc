from django.core.management import BaseCommand
from mongoengine.django.auth import User


class Command(BaseCommand):
    args = 'username password email'
    help = 'Creates a super user with credentials that you pass in'

    def handle(self, *args, **options):
        if not len(args):
            user = User.objects().create(username='admin', email='admin@admin.admin')
            user.set_password('password')
            user.save()
        else:
            user = User.objects().create(username=args[0], email=args[2])
            user.set_password(args[1])
            user.save()
        self.stdout.write('Successfully created superuser')