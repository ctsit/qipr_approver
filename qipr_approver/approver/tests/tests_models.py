import django
from django.test import TestCase
from django.test import Client
from approver.models import *
from django.core.urlresolvers import reverse
from django.db.models import fields

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
				self.assertEqual(isinstance(field,django.db.models.fields.IntegerField),True)

class BaseClassWithUserData(TestCase):
	# Insert the data through fixtures
	def setup(self):
		fixtures = ['user.json']
		self.user = User.objects.all()[0]

class BaseClassWithPersonData(BaseClassWithUserData):
	def setUp(self):
		self.user = User.objects.all()[0]
		person =  Person(last_modified_by_id=self.user,user_id=self.user,first_name="f1",last_name="l1")
		person.after_create(self.user)
		person.save(last_modified_by=user)

	def test_person(self):
		print(type(self.person))

class BaseClassWithTestData(TestCase):
	#do nothing
	print("test")

class PersonTestCase(BaseClassWithTestData):
	
	def setUp(self):
		#Create person and user
		temp = User.objects.get(username="username1")
		print("PersonTestCase:Email-" + temp.email)
		user = User(username="user1")
		user.save()
		person = Person(last_modified_by_id=user,user_id=user,first_name="f1",last_name="l1")
		person.after_create(user)
		person.save(last_modified_by=user)
		print("USER.person:" + user.person.last_name)

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

