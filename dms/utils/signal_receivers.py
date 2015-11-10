from mongoengine import post_save
from dms.models.token import Token
from dms.utils.decorators import signal_receiver

__author__ = 'asseym'


@signal_receiver(post_save)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    import pdb;pdb.set_trace()
    if created:
        Token.objects.create(user=instance)