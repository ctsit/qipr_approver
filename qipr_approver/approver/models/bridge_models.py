from django.db import models

class Registerable(models.Model):
    in_registry = models.BooleanField(default=False)

    def register(self):
        self.in_registry = True

    def is_registered(self):
        return self.in_registry

    def natural_key(self):
        natural_dict = self.get_natural_dict()
        natural_dict['guid'] = self.guid
        natural_dict['model_class_name'] = self.__class__.__name__
        return (natural_dict)

    class Meta:
        abstract = True


class PushQueue(models.Model):
    """
    This model is used to stage other models that will be pushed over later
    """
    guid = models.CharField(max_length=32)
    model_name = models.CharField(max_length=20)
