import sys

from approver.models import *
from approver.tests.tests_models.test_utils import check_fields, is_foreign_key_to

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import fields, signals
from django.test import TestCase, Client
from django.db.utils import IntegrityError

class SectionTestCase(TestCase):
    def setUp(self):
        self.user = User(username = 'testuser')
        self.user.save()

    def test_should_pass_when_model_has_correct_fields(self):
        self.assertTrue(check_fields(Section, "name", "Char"))
        self.assertTrue(check_fields(Section, "sort_order", "Integer"))

    def test_should_throw_exception_when_not_unique_sort_order(self):
        section1 = Section(name = 'section1', sort_order = 1)
        section2 = Section(name = 'section2', sort_order = 1)

        section1.save(self.user)
        self.assertRaises(IntegrityError, lambda : section2.save(self.user))

    def test_should_print_name_when_asked_for_string(self):
        text = "sample text"
        section = Section(name = text)
        self.assertEqual(str(section), text)

class QuestionTestCase(TestCase):
    def setUp(self):
        self.user = User(username = 'testuser')
        self.user.save()

    def test_should_pass_when_model_has_correct_fields(self):
        self.assertTrue(is_foreign_key_to(Question, "section", Section))
        self.assertTrue(check_fields(Question, "text", "Text"))
        self.assertTrue(check_fields(Question, "description", "Text"))
        self.assertTrue(check_fields(Question, "sort_order", "Integer"))
        self.assertTrue(is_foreign_key_to(Question, "correct_choice", Choice))
        self.assertTrue(is_foreign_key_to(Question, "choice", Choice))

    def test_should_throw_exception_when_saved_without_correct_choice(self):
        question = Question()
        self.assertRaises(IntegrityError, lambda : question.save(self.user))

    def test_should_pass_when_saving_with_user_and_correct_choice(self):
        question = Question()
        choice = Choice(text='testChoice', sort_order = 1)
        choice.save(self.user)
        question.correct_choice = choice
        question.save(self.user)
        self.assertTrue(question in Question.objects.all())

    def test_should_print_text_when_asked_for_string(self):
        text = "sample choice"
        question = Question(text = text)
        self.assertEqual(str(question), text)

class ChoiceTestCase(TestCase):
    def setUp(self):
        self.user = User(username = 'testuser')
        self.user.save()

    def test_should_pass_when_model_has_correct_fields(self):
        self.assertTrue(check_fields(Choice, "text", "Text"))
        self.assertTrue(check_fields(Choice, "sort_order", "Integer"))

    def test_should_throw_exception_when_not_unique_sort_order(self):
        choice1 = Choice(text = 'choice1', sort_order = 1)
        choice2 = Choice(text = 'choice2', sort_order = 1)

        choice1.save(self.user)
        self.assertRaises(IntegrityError, lambda : choice2.save(self.user))

    def test_should_print_text_when_asked_for_string(self):
        text = "sample choice"
        choice = Choice(text = text)
        self.assertEqual(str(choice), text)

class ResponseTestCase(TestCase):
    def setUp(self):
        self.user = User(username = 'testuser')
        self.user.save()
        self.correct_choice = Choice(text='test choice', sort_order = 1)
        self.correct_choice.save(self.user)
        self.incorrect_choice = Choice(text='test choice', sort_order = 2)
        self.incorrect_choice.save(self.user)
        self.question = Question(text='test question', correct_choice = self.correct_choice)
        self.question.save(self.user)

    def test_should_pass_when_model_has_correct_fields(self):
        self.assertTrue(is_foreign_key_to(Response, "user", User))
        self.assertTrue(is_foreign_key_to(Response, "question", Question))
        self.assertTrue(is_foreign_key_to(Response, "choice", Choice))
        self.assertTrue(is_foreign_key_to(Response, "project", Project))

    def test_should_pass_when_is_correct_response(self):
        response = Response(question = self.question, choice = self.correct_choice)
        self.assertTrue(response.is_correct_response)

    def test_should_not_be_correct_when_not_correct_choice_selected(self):
        response = Response(question = self.question, choice = self.incorrect_choice)
        self.assertTrue(response.is_correct_response)
