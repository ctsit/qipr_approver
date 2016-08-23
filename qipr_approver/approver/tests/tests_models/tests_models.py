import sys

from approver.models import *
from approver.signals.bridge.model_signals import model_push

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import fields, signals
from django.test import TestCase, Client
from approver.tests.tests_models.test_utils import check_fields, is_foreign_key_to

class OrganizationModel(TestCase):
    def setUp(self):
        signals.post_save.disconnect(model_push, Organization)
        self.user = User(username = 'testUser')
        self.user.save()

    def test_should_save_when_given_user(self):
        org = Organization(org_name='test')
        org.save(self.user)
        self.assertIn(org, Organization.objects.all())

    def test_should_not_save_when_missing_user(self):
        org = Organization(org_name='test')
        self.assertRaises(TypeError, lambda : org.save())

    def test_should_delete_when_given_user(self):
        org = Organization(org_name='test')
        org.save(self.user)
        if org in Organization.objects.all():
            org.delete(self.user)
            self.assertNotIn(org, Organization.objects.all())
        else:
            self.fail("Organization failed to save")

    def test_should_not_delete_when_missing_user(self):
        org = Organization(org_name='test')
        self.assertRaises(TypeError, lambda : org.save())

    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(Organization, "org_name", "Char", 400))

    def test_should_print_text_when_asked_for_string(self):
        org_name = "test org"
        org = Organization(org_name = org_name)

        self.assertEqual(str(org), org_name)

class TrainingModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(Training, "name", "Char", 200))

class SpecialityModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(Speciality, "name" ,"Char", 50))
        self.assertTrue(check_fields(Speciality, "description", "Char", 100))

class PositionModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(Position, "name", "Char", 50))
        self.assertTrue(check_fields(Position, "description", "Char", 100))

class KeywordModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(Keyword, "name", "Char", 50))
        self.assertTrue(check_fields(Keyword, "description", "Char", 100))

class SafetyTargetModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(SafetyTarget, "name", "Char", 50))
        self.assertTrue(check_fields(SafetyTarget, "description", "Char", 100))

class ClinicalAreaModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(ClinicalArea, "name", "Char", 50))
        self.assertTrue(check_fields(ClinicalArea, "description", "Char", 100))

class SuffixModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(Suffix, "name", "Char", 20))
        self.assertTrue(check_fields(Suffix, "description", "Char", 100))

class ExpertiseModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(Expertise, "name", "Char", 50))
        self.assertTrue(check_fields(Expertise, "description", "Char", 100))

class QIInterestModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(QI_Interest, "name", "Char", 50))
        self.assertTrue(check_fields(QI_Interest, "description", "Char", 100))

class CategoryModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(Category, "name", "Char", 50))
        self.assertTrue(check_fields(Category, "description", "Char", 100))

class BigAimModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(BigAim, "name", "Char", 100))
        self.assertTrue(check_fields(BigAim, "sort_order", "Integer"))

class FocusAreaModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(FocusArea, "name", "Char", 100))
        self.assertTrue(check_fields(FocusArea, "sort_order", "Integer"))

class ClinicalDepartmentModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(ClinicalDepartment, "name", "Char", 100))
        self.assertTrue(check_fields(ClinicalDepartment, "sort_order", "Integer"))

class AddressModel(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(is_foreign_key_to(Address, "person", Person))
        self.assertTrue(is_foreign_key_to(Address, "organization", Organization))
        self.assertTrue(check_fields(Address, "address1", "Char", 50))
        self.assertTrue(check_fields(Address, "address2", "Char", 50))
        self.assertTrue(check_fields(Address, "city", "Char", 50))
        self.assertTrue(check_fields(Address, "zip_code", "Char", 10))
        self.assertTrue(check_fields(Address, "state", "Char", 2))
        self.assertTrue(check_fields(Address, "country", "Char", 2))

    def test_should_print_text_when_asked_for_string(self):
        address1 = "1234 Sample st"
        address2 = "Ste 123"
        city = "Testville"
        state = "FL"
        zip_code = '09876'
        country = "US"
        address = Address(
            address1 = address1,
            address2 = address2,
            city = city,
            zip_code = zip_code,
            state = state,
            country = country
            )
        self.assertEqual(str(address), ' ; '.join([address1,
                                                   address2,
                                                   city,
                                                   zip_code,
                                                   state,
                                                   country]))


