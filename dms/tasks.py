import json
from celery.task import task
import requests
from requests.exceptions import RequestException
from necoc.settings import API_URL, API_TOKEN


@task
def send_bulk_sms(obj):
    try:
        _send(obj)
    except RequestException as e:
        obj.error_message = "%s: %s" % (e.__class__.__name__, str(e.message))

    obj.save()


def _send(obj):
    data = dict(phone=obj.phone_numbers, text=obj.text)
    headers = {'Authorization': 'Token ' + API_TOKEN,
               'content-type': 'application/json'}

    response = requests.post(API_URL, data=json.dumps(data), headers=headers)
    _add_logs(response, obj)


def _add_logs(response, obj):
    response_data = response.json()
    _status_code = response.status_code
    if _status_code == 201:
        obj.rapid_pro_id = response_data['sms'][0]
    else:
        obj.error_message = "%d: %s" % (_status_code, str(response_data))