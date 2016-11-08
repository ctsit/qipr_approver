import sys, time
from datetime import datetime, timedelta

from approver.models import *
from approver.signals.bridge.model_signals import model_push
from approver.tests.tests_models.test_utils import check_fields, is_foreign_key_to

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import fields, signals
from django.test import TestCase, Client
from unittest.mock import patch
from django.utils import timezone

class ProjectTestCase(TestCase):
    def setUp(self):
        signals.post_save.disconnect(model_push, Project)
        self.user = User(username='testUser')
        self.user.save()

    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(Project,"title","Char",300))
        self.assertTrue(check_fields(Project,"description","Text"))
        self.assertTrue(is_foreign_key_to(Project, "advisor", Person))
        self.assertTrue(is_foreign_key_to(Project, "big_aim", BigAim))
        self.assertTrue(is_foreign_key_to(Project, "category", Category))
        self.assertTrue(is_foreign_key_to(Project, "clinical_area", ClinicalArea))
        self.assertTrue(is_foreign_key_to(Project, "clinical_setting", ClinicalSetting))
        self.assertTrue(is_foreign_key_to(Project, "collaborator", Person))
        self.assertTrue(is_foreign_key_to(Project, "keyword", Keyword))
        self.assertTrue(is_foreign_key_to(Project, "owner", Person))
        self.assertTrue(check_fields(Project, "approval_date", "DateTime"))
        self.assertTrue(check_fields(Project, "proposed_end_date", "DateTime"))
        self.assertTrue(check_fields(Project, "proposed_start_date", "DateTime"))

    def test_should_print_text_when_asked_for_string(self):
        title = 'test title'
        owner = Person(first_name='first', last_name='last', email_address='email')
        project = Project(title=title, owner=owner)
        test_string = ' '.join([title, str(owner)])

        self.assertEqual(str(project), test_string)

    def test_should_be_approved_when_approved(self):
        project = Project()
        project.approve(self.user)

        self.assertTrue(project.is_approved())

    def test_should_be_approved_when_in_registry(self):
        project = Project()
        project.register()

        self.assertTrue(project.is_approved())

    def test_should_not_be_approved_when_not_in_registry_or_approved(self):
        project = Project()
        self.assertFalse(project.is_approved())

    def test_should_be_editable_when_new(self):
        project = Project()
        project.save(self.user)
        self.assertTrue(project.get_is_editable())

    def test_should_not_be_editable_when_approved(self):
        project = Project()
        project.approve(self.user)
        self.assertFalse(project.get_is_editable())

    def test_should_not_be_editable_when_in_registry(self):
        project = Project()
        project.save(self.user)
        project.register()
        self.assertFalse(project.get_is_editable())

    def test_should_not_be_editable_when_older_than_a_year(self):
        previous_saved_time = timezone.now() - timedelta(days=400)

        with patch.object(timezone, 'now', return_value=previous_saved_time):
            project = Project()
            project.save(self.user)

        self.assertFalse(project.get_is_editable())
