from django.db import models

class Registerable(models.Model):
    in_registry = models.BooleanField(default=False)

    def register(self):
        self.in_registry = True

    class Meta:
        abstract = True
