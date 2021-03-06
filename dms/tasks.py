import json
from celery.task import task
from django.core.mail import send_mail
import requests
from requests.exceptions import RequestException
from necoc.settings import API_URL, API_TOKEN


@task
def send_bulk_sms(obj, phone_numbers=[], text=""):

    try:
        phone_numbers = phone_numbers or getattr(obj, 'phone_numbers', [])
        text = text or getattr(obj, 'text', '')
        response = _send(phone_numbers, text)
        _log(response, obj)
    except RequestException as e:
        obj.log = "%s: %s" % (e.__class__.__name__, str(e.message))

    obj.save()


@task
def send_one_sms(obj, phone='', text=""):

    try:
        phone = phone or getattr(obj, 'phone', '')
        text = text or getattr(obj, 'text', '')
        response = _sendone(phone, text)
        _log(response, obj)
    except RequestException as e:
        obj.log = "%s: %s" % (e.__class__.__name__, str(e.message))

    obj.save()


def _sendone(phone, text):
    data = dict(phone=phone, text=text)
    headers = {'Authorization': 'Token ' + API_TOKEN,
               'content-type': 'application/json'}
    return requests.post(API_URL, data=json.dumps(data), headers=headers)


def _send(phone_numbers, text):
    data = dict(phone=phone_numbers, text=text)
    headers = {'Authorization': 'Token ' + API_TOKEN,
               'content-type': 'application/json'}
    return requests.post(API_URL, data=json.dumps(data), headers=headers)


def _log(response, obj):
    response_data = response.json()
    status_code = response.status_code
    if status_code == 201:
        obj.log = "%d: %s = %s" % (status_code, 'rapid_pro_id', response_data['sms'][0])
    else:
        obj.log = "%d: %s" % (status_code, str(response_data))

@task
def send_email(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)