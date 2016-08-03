from django.db import models
from django.core import serializers
from django.contrib.auth.models import User
from django.db.models.signals import post_init, post_save, pre_delete

from approver.utils import get_id_or_none
from approver.models import Person

class AuditTrail(models.Model):
    user = models.ForeignKey(User, related_name='audit')
    datetime = models.DateTimeField(auto_now=True, editable=False)
    json_before = models.TextField(null=True)
    json_after = models.TextField(null=True)

    def __str__(self):
        return (str(self.user) + str(self.datetime))

    def jsonify(self, model):
        return serializers.serialize('json', [model])


def generate_json_before(**kwargs):
    instance = kwargs.get('instance')
    instance.audit_trail = AuditTrail()
    if get_id_or_none(instance):
        instance.audit_trail.json_before = instance.audit_trail.jsonify(instance)

def generate_json_after(**kwargs):
    instance = kwargs.get('instance')
    instance.audit_trail.json_after = instance.audit_trail.jsonify(instance)
    # the following two lines are busted
    # we need the user making the change not the user
    # that is being changed
    if isinstance(instance, User):
        instance.audit_trail.user = instance
    instance.audit_trail.save()

qipr_Models = [User, Person]

for qipr_Model in qipr_Models:
    post_init.connect(generate_json_before, qipr_Model)
    post_save.connect(generate_json_after, qipr_Model)
    pre_delete.connect(generate_json_after, qipr_Model)
