import re
from django.conf import settings


def split_text(message):
    # separator = getattr(settings, "MESSAGE_SEPARATOR", ".")
    # split_message = message.split(separator)
    try:
        split_message = re.findall(r"[\w']+", message)
    except TypeError:
        split_message = []
    return map(lambda x: x.strip(), split_message)
