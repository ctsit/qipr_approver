from django.db import models
from django.contrib.auth.models import User

from approver.models import Provenance, Project

class TextPrint(models.Model):
    def __str__(self):
        return self.text

    class Meta:
        abstract = True


class Section(Provenance):
    name = models.CharField(max_length=30)
    sort_order = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return self.name

class Choice(Provenance, TextPrint):
    text = models.TextField()
    sort_order = models.IntegerField(null=True, unique=True)

class Question(Provenance, TextPrint):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='question', null=True)
    text = models.TextField()
    description = models.TextField(null=True)
    sort_order = models.IntegerField(null=True, unique=True)
    choice = models.ManyToManyField(Choice, related_name='question')
    correct_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='+')

class Response(Provenance):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='response')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='response')

    def is_correct_response(self):
        """
        This will eventually need to check against something to tell if
        this is a response that lets people get approved
        """
        if self.choice == self.question.correct_choice:
            return True

        return False
