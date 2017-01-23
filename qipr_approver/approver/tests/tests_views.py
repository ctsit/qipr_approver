from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        self.client = None

    # these need to work with fake shib
    # def test_dashboard_redirects_without_login(self):
    #     response = self.client.get('/dashboard/')
    #     self.assertEqual(response.status_code,302)

    # def test_add_project_redirects_without_login(self):
    #     response = self.client.get('/projects/')
    #     self.assertEqual(response.status_code,302)
