from django.db import models
from approver.models.bridge_models import Registerable

class TaggedWithName(models.Model):
    tag_property_name = 'name'

    class Meta:
        abstract = True

class TagPrint(models.Model):
    def __str__(self, delimiter=' '):
        return delimiter.join([self.name, self.description or ''])

    class Meta:
        abstract = True

class Tag(TaggedWithName, TagPrint, Registerable):
    """
    The class that all Tags are based off of.
    A model is a Tag if it contains:

    name: the name of the tag
    description: the developer's way of understanding the tag
    __str__: Inherited from the TagPrint class
    tag_property_name: always of value 'name'
    get_natural_dict: returns a dictionary describing the tag

    Also Tags are registerable with the registry
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True)

    def get_natural_dict(self):
        return {
            'name': str(self.name),
            'description': str(self.description),
        }

    class Meta:
        abstract = True

