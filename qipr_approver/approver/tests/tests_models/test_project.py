import sys

from approver.models import *
from approver.signals.bridge.model_signals import model_push

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import fields, signals
from django.test import TestCase, Client

class ProjectTestCase(TestCase):
    def setUp(self):
        signals.post_save.disconnect(model_push, Project)
        pass

    def test_project_model(self):
        project = Project()
        for field in Project._meta.fields:
            if field.name in "title":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 300)
            if field.name in ["description"]:
                self.assertEqual(isinstance(field, django.db.models.fields.TextField), True)
