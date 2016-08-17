import sys

from approver.models import *
from approver.signals.bridge.model_signals import model_push

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import fields, signals
from django.test import TestCase, Client
from approver.utils import check_fields as check_fields

class OrganizationModel(TestCase):
    def test_organization_model(self):
        org = Organization()
        for field in Organization._meta.fields:
            if field.name in "title":
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length, 30)

class SpecialityModel(TestCase):
    def test_speciality_model(self):
        self.assertEqual(check_fields(Speciality,"name","Char",50), True)

class PositionModel(TestCase):
    def test_position_model(self):
        self.assertEqual(check_fields(Position,"name","Char",50), True)

class KeywordModel(TestCase):
    def test_keyword_model(self):
        self.assertEqual(check_fields(Keyword,"name","Char",50), True)

class SafetyTargetModel(TestCase):
    def test_safety_target_model(self):
        self.assertEqual(check_fields(SafetyTarget,"name","Char",50), True)
        self.assertEqual(check_fields(SafetyTarget,"description","Char",100), True)

class ClinicalAreaModel(TestCase):
    def test_clinical_area_model(self):
        self.assertEqual(check_fields(ClinicalArea,"name","Char",50), True)
        self.assertEqual(check_fields(ClinicalArea,"description","Char",100), True)

class SuffixModel(TestCase):
    def test_suffix_model(self):
        self.assertEqual(check_fields(Suffix,"name","Char",20), True)
        self.assertEqual(check_fields(Suffix,"description","Char",100), True)

class QIInterestModel(TestCase):
    def test_qi_interest_model(self):
        self.assertEqual(check_fields(QI_Interest,"name","Char",50), True)
        self.assertEqual(check_fields(QI_Interest,"description","Char",100), True)

class CategoryModel(TestCase):
    def test_category_model(self):
        self.assertEqual(check_fields(Category,"name","Char",50), True)
        self.assertEqual(check_fields(Category,"description","Char",100), True)

class BigAimModel(TestCase):
    def test_big_aim_model(self):
        self.assertEqual(check_fields(BigAim,"name","Char",100), True)

class FocusAreaModel(TestCase):
    def test_focus_area_model(self):
        self.assertEqual(check_fields(FocusArea,"name","Char",100), True)

class ClinicalDepartmentModel(TestCase):
    def test_clinical_department_model(self):
        self.assertEqual(check_fields(ClinicalDepartment,"name","Char",100), True)