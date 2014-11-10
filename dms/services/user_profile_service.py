from mongoengine.django.auth import User
from mongoengine.django.auth import UserManager
from django.conf import settings
from django.core.mail import send_mail
from dms.tasks import send_new_user_email
from necoc.settings import HOSTNAME


class UserProfileService(object):

    @classmethod
    def setup_new_user(cls, username, name, email):
        user = User(username=username).save()
        password = cls.set_new_password(user)
        message = cls.build_email_message(name, username, password)
        send_new_user_email.delay('Your NECOC Account', message, settings.DEFAULT_FROM_EMAIL, [email])
        return user

    @classmethod
    def set_new_password(cls, user):
        password = UserManager().make_random_password()
        user.set_password(password)
        return password

    @classmethod
    def build_email_message(cls, name, username, password):
        message = """
                Dear %s,

                Your email was recently registered for NECOC DMS.
                Please use the following credentials to login to %s

                username: %s
                password: %s

                Thank you,
                NECOC DMS team
                """
        return message % (name, HOSTNAME, username, password)