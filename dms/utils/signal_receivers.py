from django.conf import settings
from django.db.models.loading import get_app
from dms.tasks import send_email

__author__ = 'asseym'


def associate_disaster(sender, instance=None, created=False, **kwargs):
    app = get_app('dms')
    dModel = app.disaster.Disaster
    dTModel = app.disaster_type.DisasterType
    if sender.__name__ == 'RapidProMessage':
        if created:
            instance = kwargs.get('document')
            disaster = instance.disaster or instance._associate_to_disaster()
            if disaster and type(disaster) == str:
                disaster_type = dTModel.objects(**dict(name=disaster)).order_by('-created_at').first()
                locs = instance.location.full_tree()
                disaster_obj = dModel.objects(**dict(name=disaster_type, locations__in=locs))\
                    .order_by('-created_at').first()
                instance.disaster = disaster_obj
                if disaster_obj:
                    instance.auto_associated = True
                instance.save()


def add_yesno_categories_to_poll(sender, instance=None, created=False, **kwargs):
    if sender.__name__ == 'Poll':
        if created:
            instance = kwargs.get('document')
            if instance.ptype == 'yesno':
                sender.add_yesno_categories(instance)


def categorise_yesno_response(sender, instance=None, created=False, **kwargs):
    if sender.__name__ == 'PollResponse':
        if created:
            instance = kwargs.get('document')
            if instance.poll and instance.poll.ptype == 'yesno':
                sender.process_response(instance)


def auto_close_old_polls(sender, instance=None, created=False, **kwargs):
    always_open = settings.ALWAYS_OPEN_POLLS
    if sender.__name__ == 'Poll':
        if created:
            instance = kwargs.get('document')
            open_polls = sender.objects(open=True).order_by('-created_at')
            if open_polls.count() > always_open:
                to_close = open_polls[always_open:(always_open+1)]
                open_polls.filter(id__in=[to_close[0].id]).update(set__open=False)
                # to_close.update(set__open=False)


def notify_new_disaster_status(sender, instance=None, created=False, **kwargs):
    if sender.__name__ == 'Disaster':
        if not created:
            instance = kwargs.get('document')
            if instance.pk is not None:
                orig = sender.objects.get(pk=instance.pk)
                if not orig.status == instance.status:
                    name = 'DMS User'
                    subject = 'Status of Disaster Risk has changed'
                    from_email = settings.DEFAULT_FROM_EMAIL
                    locations = [loc.name for loc in instance.locations]
                    message = settings.DISASTER_STATUS_CHANGE_MESSAGE % \
                              {'name': name,
                               'disaster_name': instance.name.name,
                               'locations': '['+ ','.join(locations)+']',
                               'original_status': orig.status,
                               'new_status': instance.status}
                    recipient_list = settings.DISASTER_NOTIFY_STATUS
                    send_email.delay(subject, message, from_email, recipient_list)