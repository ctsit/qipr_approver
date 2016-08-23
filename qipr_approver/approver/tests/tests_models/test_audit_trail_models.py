import django, datetime

from django.test import TestCase

from approver.models import *
from approver.tests.tests_models.test_utils import check_fields, is_foreign_key_to

class AuditTrailTestCase(TestCase):
    def test_should_have_proper_fields_when_created(self):
        self.assertTrue(check_fields(AuditTrail, "datetime", "DateTime"))
        self.assertTrue(check_fields(AuditTrail, "json_before", "Text"))
        self.assertTrue(check_fields(AuditTrail, "json_after", "Text"))
        self.assertTrue(is_foreign_key_to(AuditTrail, "user", User))

    def test_should_print_text_when_when_asked_for_string(self):
        user = User(username='testUser')
        date = datetime.datetime.now()
        audit = AuditTrail(user=user, datetime=date)
        self.assertEqual(str(audit), str(user) + str(date))
