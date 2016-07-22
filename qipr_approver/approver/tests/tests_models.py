from django.test import TestCase
from django.test import Client
from approver.models import *
from django.core.urlresolvers import reverse

class BaseClassWithTestData(TestCase):
	fixtures = ['dump_admin.json']
	user = User.objects.get(username="username1")
	print("BaseClassWithTestData:Email- " + user.email)
	person = Person.objects.get(first_name="qweqw")
	#print("Person LastName:" + user.person.last_name)


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

