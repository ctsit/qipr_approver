import sys

from approver.models import *
from approver.signals.bridge.model_signals import model_push

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import fields, signals
from django.test import TestCase, Client
from approver.tests.tests_models.test_utils import check_fields

class OrganizationModel(TestCase):
    def test_organization_model(self):
        org = Organization()
        for field in Organization._meta.fields:
            if field.name in "title":
                self.assertTrue(isinstance(field, django.db.models.fields.CharField), True)
                self.assertTrue(field.max_length, 30)

class SpecialityModel(TestCase):
    def test_speciality_model(self):
        self.assertTrue(check_fields(Speciality,"name","Char",50))

class PositionModel(TestCase):
    def test_position_model(self):
        self.assertTrue(check_fields(Position,"name","Char",50))

class KeywordModel(TestCase):
    def test_keyword_model(self):
        self.assertTrue(check_fields(Keyword,"name","Char",50))

class SafetyTargetModel(TestCase):
    def test_safety_target_model(self):
        self.assertTrue(check_fields(SafetyTarget,"name","Char",50))
        self.assertTrue(check_fields(SafetyTarget,"description","Char",100))

class ClinicalAreaModel(TestCase):
    def test_clinical_area_model(self):
        self.assertTrue(check_fields(ClinicalArea,"name","Char",50))
        self.assertTrue(check_fields(ClinicalArea,"description","Char",100))

class SuffixModel(TestCase):
    def test_suffix_model(self):
        self.assertTrue(check_fields(Suffix,"name","Char",20), True)
        self.assertTrue(check_fields(Suffix,"description","Char",100))

class QIInterestModel(TestCase):
    def test_qi_interest_model(self):
        self.assertTrue(check_fields(QI_Interest,"name","Char",50))
        self.assertTrue(check_fields(QI_Interest,"description","Char",100))

class CategoryModel(TestCase):
    def test_category_model(self):
        self.assertTrue(check_fields(Category,"name","Char",50))
        self.assertTrue(check_fields(Category,"description","Char",100))

class BigAimModel(TestCase):
    def test_big_aim_model(self):
        self.assertTrue(check_fields(BigAim,"name","Char",100))

class FocusAreaModel(TestCase):
    def test_focus_area_model(self):
        self.assertTrue(check_fields(FocusArea,"name","Char",100))

class ClinicalDepartmentModel(TestCase):
    def test_clinical_department_model(self):
        self.assertTrue(check_fields(ClinicalDepartment,"name","Char",100))