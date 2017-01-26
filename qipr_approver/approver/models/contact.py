from datetime import timedelta

from django.db import models
from django.utils import timezone

from approver import utils
from approver import constants
from approver.models.bridge_models import Registerable
from approver.models.provenance import Provenance
from approver.models import Person


class Contact(Provenance, Registerable):
    business_email = models.CharField(max_length=100, null=True)
    business_fax = models.CharField(max_length=20, null=True)
    business_phone = models.CharField(max_length=50, null=True)
    display_name = models.CharField(max_length=70)
    first_name = models.CharField(max_length=30)
    gatorlink = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    name_prefix = models.CharField(max_length=30)
    name_suffix = models.CharField(max_length=30)
    working_title = models.CharField(max_length=30)

    person = models.ForeignKey(Person, null=True)

    tag_property_name = 'business_email'

    def save(self, *args, **kwargs):
        try:
            for char in constants.invalid_email_characters:
                self.business_email = self.business_email.replace(char, '')
        except:
            pass
        super(Contact, self).save(*args, **kwargs)

    def __str__(self):
        first = self.first_name or ''
        last = self.last_name or ''
        name = ', '.join([str(item) for item in [first, last] if len(item)])
        email = '(' +self.business_email + ')' if self.business_email else ''
        return ' '.join([name, email])

    def get_natural_dict(self):
        return {
            'gatorlink': self.gatorlink,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'business_email': self.business_email,
            'model_class_name': self.__class__.__name__,
        }

