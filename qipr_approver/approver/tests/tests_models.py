import sys

from approver.models import *
from approver.signals.bridge.model_signals import model_push

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import fields, signals
from django.test import TestCase, Client

class PersonModel(TestCase):
    def test_person_model(self):
        person = Person()
        for field in Person._meta.fields:
            if field.name in ["first_name","last_name"]:
                self.assertEqual(isinstance(field,django.db.models.fields.CharField),True)
                self.assertEqual(field.max_length,30)
            if field.name in ["webpage_url","email_address"]:
                self.assertEqual(isinstance(field,django.db.models.fields.CharField),True)
            if field.name in ["business_phone","contact_phone"]:
                self.assertEqual(isinstance(field,django.db.models.fields.CharField),True)

class ProjectModel(TestCase):
    def test_project_model(self):
        project = Project()
        for field in Project._meta.fields:
            if field.name in "title":
                self.assertEqual(isinstance(field,django.db.models.fields.CharField),True)
                self.assertEqual(field.max_length,300)
            if field.name in ["description"]:
                self.assertEqual(isinstance(field,django.db.models.fields.TextField),True)

class OrganizationModel(TestCase):
    def test_organization_model(self):
        org = Organization()
        for field in Organization._meta.fields:
            if field.name in "title":
                self.assertEqual(isinstance(field,django.db.models.fields.CharField),True)
                self.assertEqual(field.max_length,30)

class SpecialityModel(TestCase):
    def test_speciality_model(self):
        spec = Speciality()
        for field in Speciality._meta.fields:
            if field.name in "name":
                self.assertEqual(isinstance(field,django.db.models.fields.CharField),True)
                self.assertEqual(field.max_length,50)

class PositionModel(TestCase):
    def test_position_model(self):
        pos = Position()
        for field in Position._meta.fields:
            if field.name in "name":
                self.assertEqual(isinstance(field,django.db.models.fields.CharField),True)
                self.assertEqual(field.max_length,50)

class BaseClassWithUserData(TestCase):
    # Insert the data through fixtures
    def setUp(self):
        fixtures = ['user.json']
        print(User.objects.all())
        self.user = User.objects.all()[0]

class BaseClassWithPersonData(BaseClassWithUserData):
    def setUp(self):
        self.user = User.objects.all()[0]
        person =  Person(last_modified_by_id=self.user,user_id=self.user,first_name="f1",last_name="l1")
        person.after_create(self.user)
        person.save(last_modified_by=user)

class BaseClassWithTestData(TestCase):
    #do nothing
    print("test")
    pass

class PersonTestCase(BaseClassWithTestData):
    def setUp(self):
        signals.post_save.disconnect(model_push, Person)
        self.user = User(username='testuser')
        self.user.save()
        self.person = Person()

    def test_person_needs_user_to_save(self):
        self.assertRaises(TypeError, lambda : self.person.save())
        try:
            self.person.save(self.user)
        except:
            self.fail('The person failed to save with user. Exception:' + str(sys.exc_info()))

    def test_is_person_created(self):
        user = User.objects.get(username="user1")
        person = Person.objects.get(user_id = user)
        self.assertEqual(person.first_name,'f1')
        self.assertEqual(person.user_id.username,"user1")

class ProjectTestCase(BaseClassWithTestData):
    def setUp(self):
        print("In ProjectTestCase")

    def test_is_project_created(self):
        person=Person.objects.all()[0]
        project = Project(title="Project1",owner=person)
        project.after_create(user)
        project.save(last_modified_by=user)
        print("Created project with title: " + Project.objects.get(title="Project1"))
