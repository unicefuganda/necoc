from django.db.models.loading import get_app
from dms.utils.decorators import signal_receiver

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
                disaster_obj = dModel.objects(**dict(name=disaster_type, locations=instance.location))\
                    .order_by('-created_at').first()
                instance.disaster = disaster_obj
                if disaster_obj:
                    instance.auto_associated = True
                instance.save()