from django.db.models.signals import post_save

from approver.bridge import push_model
from approver.signals import AllRegistryModels
from approver.decorators import disable_for_loaddata

@disable_for_loaddata
def model_push(**kwargs):
    instance = kwargs.get('instance')

    if __is_project(instance):
        if instance.is_approved():
            push_model(instance)
    else:
        push_model(instance)

def __is_project(model):
    return model.__class__.__name__ == "Project"

def connect_model_signals():
    for model in AllRegistryModels:
        post_save.connect(model_push, model)

def disconnect_for_loading():
    for model in AllRegistryModels:
        post_save.disconnect(model_push, model)
