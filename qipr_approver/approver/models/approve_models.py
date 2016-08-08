from django.db import models
from django.contrib.auth.models import User

from approver.models import Provenance, NamePrint, Project

class TextPrint(models.Model):
    def __str__(self):
        return self.text

    class Meta:
        abstract = True


class Section(Provenance, NamePrint):
    name = models.CharField(max_length=30)
    sort_order = models.IntegerField(unique=True)

class Question(Provenance, TextPrint):
    section = models.ForeignKey(Section, related_name='question', null=True)
    text = models.TextField()
    description = models.TextField(null=True)
    sort_order = models.IntegerField()

class Choice(Provenance, TextPrint):
    question = models.ManyToManyField(Question, related_name='choice')
    text = models.TextField()
    sort_order = models.IntegerField()

class Response(Provenance):
    user = models.ForeignKey(User, related_name='response')
    question = models.ForeignKey(Question)
    choice = models.ForeignKey(Choice)
    project = models.ForeignKey(Project, related_name='response')

    def is_valid(self):
        """
        This will eventually need to check against something to tell if
        this is a response that lets people get approved
        """
        return False
