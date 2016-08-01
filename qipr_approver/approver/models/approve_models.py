from django.db import models
from django.contrib.auth.models import User

from approver.models import Provenance, NamePrint, TaggedWithName, Project

class TextPrint(models.Model):
    def __str__(self):
        return self.text

    class Meta:
        abstract = True


class Section(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=30)
    sort_order = models.IntegerField(unique=True)

class Question(Provenance, TextPrint):
    section = models.ForeignKey(Section, related_name='question', null=True)
    text = models.TextField()
    description = models.TextField(null=True)
    sort_order = models.IntegerField()

class Choice(Provenance, TextPrint):
    question = models.ForeignKey(Question, related_name='choice')
    text = models.TextField()
    sort_order = models.IntegerField()

class Response(Provenance):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    choice = models.ForeignKey(Choice)
    project = models.ForeignKey(Project)
    free_text_response = models.TextField()
