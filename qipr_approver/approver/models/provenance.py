from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from approver.constants import STATE_CHOICES, COUNTRY_CHOICES, QI_CHECK
from approver import utils

class Provenance(models.Model):
    created_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, related_name="+")
    last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=True)
    guid = models.CharField(max_length=32, default=utils.get_guid, editable=False)

    def save(self, last_modified_by, *args, **kwargs):
        utils.set_created_by_if_empty(self, last_modified_by)
        try:
            self.audit_trail.user = last_modified_by
        except:
            pass
        utils.set_guid_if_empty(self)
        self.last_modified_by = last_modified_by
        super(Provenance, self).save(*args, **kwargs)

    def delete(self, last_modified_by, *args, **kwargs):
        try:
            self.audit_trail.user = last_modified_by
        except:
            pass
        self.last_modified_by = last_modified_by
        super(Provenance, self).delete(*args, **kwargs)

    class Meta:
        abstract = True
