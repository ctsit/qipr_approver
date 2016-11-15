from django.db import models
from django.utils import timezone

class Registerable(models.Model):
    in_registry = models.BooleanField(default=False)
    date_first_registered = models.DateTimeField(null=True)

    def register(self):
        self.date_first_registered = timezone.now()

    def natural_key(self):
        natural_dict = self.get_natural_dict()
        natural_dict['guid'] = self.guid
        natural_dict['model_class_name'] = self.__class__.__name__
        return (natural_dict)

    class Meta:
        abstract = True
