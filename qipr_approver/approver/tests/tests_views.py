from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

class TestView(TestCase):
	#Initial login takes user to AboutYou
	#Re-login takes user to Dashboard
	client = Client()
	def test_shib(self):
		response = self.client.post('/shib/', {'username': 'test','password':'temp','gatorlink':'test'})
		print(response)
		self.assertEqual(response.status_code,302)
		self.assertEqual(response.url, '/aboutyou/')
		response1 = self.client.post('/shib/', {'username': 'test','password':'temp','gatorlink':'test'})
		print(response1)
		self.assertEqual(response1.status_code,302)
		self.assertEqual(response1.url, '/dashboard/')

	def test_dashboard(self):
		response = self.client.get('/dashboard/')
		self.assertEqual(response.status_code,302)
		print(response)
		
	def test_add_project(self):
		response = self.client.get('/projects/')
		self.assertEqual(response.status_code,302)
		print(response)
