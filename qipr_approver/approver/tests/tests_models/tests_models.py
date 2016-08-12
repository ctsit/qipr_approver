import sys

from approver.models import *
from approver.signals.bridge.model_signals import model_push

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import fields, signals
from django.test import TestCase, Client

class OrganizationModel(TestCase):
    def test_organization_model(self):
        org = Organization()
        for field in Organization._meta.fields:
            if field.name in "title":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 30)

class SpecialityModel(TestCase):
    def test_speciality_model(self):
        spec = Speciality()
        for field in Speciality._meta.fields:
            if field.name in "name":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 50)

class PositionModel(TestCase):
    def test_position_model(self):
        pos = Position()
        for field in Position._meta.fields:
            if field.name in "name":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 50)
