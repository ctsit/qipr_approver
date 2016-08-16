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

class KeywordModel(TestCase):
    def test_position_model(self):
        keyword = Keyword()
        for field in Keyword._meta.fields:
            if field.name in "name":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 50)

class QIInterestModel(TestCase):
    def test_category_model(self):
        for field in QI_Interest._meta.fields:
            if field.name in "name":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 50)
            if field.name in "description":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 100)

class CategoryModel(TestCase):
    def test_category_model(self):
        for field in Category._meta.fields:
            if field.name in "name":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 50)
            if field.name in "description":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 100)

class BigAimModel(TestCase):
    def test_big_aim_model(self):
        bigaim = BigAim()
        for field in BigAim._meta.fields:
            if field.name in "name":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 100)

class PositionModel(TestCase):
    def test_focus_area_model(self):
        fa = FocusArea()
        for field in FocusArea._meta.fields:
            if field.name in "name":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 100)

class ClinicalDepartmentModel(TestCase):
    def test_clinical_department_model(self):
        cd = ClinicalDepartment()
        for field in ClinicalDepartment._meta.fields:
            if field.name in "name":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 100)