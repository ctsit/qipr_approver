from django.db.models.signals import post_save

from approver.models import Project
from approver.bridge import push_model
from approver.signals import AllRegistryModels

def model_push(**kwargs):
    instance = kwargs.get('instance')
    if not instance.in_registry:
        push_model(instance)

def connect_project_signals():
    for model in AllRegistryModels:
        post_save.connect(model_push, model)
