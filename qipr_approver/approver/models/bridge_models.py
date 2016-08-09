from django.db import models

class Registerable(models.Model):
    in_registry = models.BooleanField(default=False)

    def register(self):
        self.in_registry = True

    def natural_key(self):
        natural_dict = self.get_natural_dict()
        natural_dict['guid'] = self.guid
        natural_dict['model_class_name'] = self.__class__.__name__
        return (natural_dict)

    class Meta:
        abstract = True
