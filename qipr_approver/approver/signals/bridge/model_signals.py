from django.db.models.signals import post_save

from approver.bridge import push_model
from approver.signals import AllRegistryModels
from approver.decorators import disable_for_loaddata

@disable_for_loaddata
def model_push(**kwargs):
    instance = kwargs.get('instance')
    if not instance.in_registry:
        push_model(instance)

def connect_model_signals():
    for model in AllRegistryModels:
        post_save.connect(model_push, model)
