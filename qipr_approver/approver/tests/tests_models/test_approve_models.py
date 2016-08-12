import sys

from approver.models import *

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import fields, signals
from django.test import TestCase, Client

class SectionTestCase(TestCase):
    def setUp(self):
        pass

    def test_no_section_tests_written(self):
        self.fail('You have not written any tests for {}'.format(type(self)))

class QuestionTestCase(TestCase):
    def setUp(self):
        pass

    def test_no_question_tests_written(self):
        self.fail('You have not written any tests for {}'.format(type(self)))

class ChoiceTestCase(TestCase):
    def setUp(self):
        pass

    def test_no_choice_tests_written(self):
        self.fail('You have not written any tests for {}'.format(type(self)))

class ResponseTestCase(TestCase):
    def setUp(self):
        pass

    def test_no_response_tests_written(self):
        self.fail('You have not written any tests for {}'.format(type(self)))

