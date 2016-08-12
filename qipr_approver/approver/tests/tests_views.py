from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        self.client = None

    def test_shib_first_and_second_login(self):
        response = self.client.post('/shib/', {'username': 'test','password':'temp','gatorlink':'test'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url, '/aboutyou/')
        response1 = self.client.post('/shib/', {'username': 'test','password':'temp','gatorlink':'test'})
        self.assertEqual(response1.status_code,302)
        self.assertEqual(response1.url, '/dashboard/')

    def test_dashboard_redirects_without_login(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code,302)

    def test_add_project_redirects_without_login(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code,302)
