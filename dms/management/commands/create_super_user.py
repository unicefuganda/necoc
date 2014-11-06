from django.core.management import BaseCommand
from mongoengine.django.auth import User


class Command(BaseCommand):
    args = 'username password email'
    help = 'Creates a super user with credentials that you pass in'

    def handle(self, *args, **options):
        if not len(args):
            user = User(username='admin', email='admin@admin.admin').save()
            user.set_password('password')
        else:
            user = User(username=args[0], email=args[2]).save()
            user.set_password(args[1])
        self.stdout.write('Successfully created superuser')