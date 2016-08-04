from django.db.models.signals import post_init, post_save, pre_delete
from django.core import serializers

from approver.models import AuditTrail
from approver.utils import get_id_or_none
from approver.signals import AllNormalModels

def jsonify(model_instance):
    return serializers.serialize('json', [model_instance])

def generate_json_before(**kwargs):
    instance = kwargs.get('instance')
    instance.audit_trail = AuditTrail()
    if get_id_or_none(instance):
        instance.audit_trail.json_before = jsonify(instance)

def generate_json_after(**kwargs):
    instance = kwargs.get('instance')
    instance.audit_trail.json_after = jsonify(instance)
    instance.audit_trail.save()

def on_pre_delete(**kwargs):
    empty_json_fixture = '[]'
    instance = kwargs.get('instance')
    instance.audit_trail.json_after = empty_json_fixture
    instance.audit_trail.save()

def connect_signals():
    for qipr_Model in AllNormalModels:
        post_init.connect(generate_json_before, qipr_Model)
        post_save.connect(generate_json_after, qipr_Model)
        pre_delete.connect(on_pre_delete, qipr_Model)
