import json
from celery.task import task
import requests
from necoc.settings import API_URL, API_TOKEN


@task
def send_bulk_sms(obj):
    data = dict(phone=obj.phone_numbers, text=obj.text)
    headers = {'Authorization': 'Token ' + API_TOKEN,
               'content-type': 'application/json'}
    try:
        response = requests.post(API_URL, data=json.dumps(data), headers=headers)
        response_data = json.loads(response.content)
        obj.rapid_pro_id = response_data['sms'][0]
    except Exception as e:
        obj.error_message = str(e.message)

    obj.save()
