from django.test import TestCase
from django.contrib.auth.models import User
from approver.models import Person,Project
from approver.workflows import project_crud

class ProjectWorkFlowTestCase(TestCase):
	def setUp(self):
		"""
		Create test data for user,person,project for testing project_crud workflow.
		"""
		self.user = User(username='testuser')
		self.user.save()
		self.person = Person(user= self.user,first_name = 'first', last_name = 'last', email_address = 'email')
		self.person.save(last_modified_by=self.user)
		self.project = Project(title = "testproj", owner = self.person)
		self.project.save(last_modified_by=self.user)

	def test_get_project_should_not_return_none(self):
		projects = Project.objects.all()
		for project in projects:
			self.assertNotEqual(project_crud.get_project_or_none(project.id),None)

	def test_get_project_should_return_none(self):
		self.assertEqual(project_crud.get_project_or_none(-1),None)

	def test_project_should_exists(self):
		projects = Project.objects.all()
		for project in projects:
			self.assertEqual(project_crud.project_exists(project.id),True)

	def test_project_exists(self):
		self.assertEqual(project_crud.project_exists(-1),False)

	def test_current_user_is_project_owner(self):
		self.assertTrue(project_crud.current_user_is_project_owner(self.user,self.project))

	def test_current_user_is_project_advisor_or_collaborator(self):
		self.assertFalse(project_crud.current_user_is_project_advisor_or_collaborator(self.user,self.project))

	def test_current_user_can_perform_project_delete(self):
		self.assertTrue(project_crud.current_user_can_perform_project_delete(self.user,self.project))
