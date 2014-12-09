
from django.conf import settings


def split_text(message):
    separator = getattr(settings, "MESSAGE_SEPARATOR", ".")
    split_message = message.split(separator)
    return map(lambda x: x.strip(), split_message)
