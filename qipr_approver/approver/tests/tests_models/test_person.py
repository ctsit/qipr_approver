import sys

from approver.models import *
from approver.signals.bridge.model_signals import model_push

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import fields, signals
from django.test import TestCase, Client

class PersonTestCase(TestCase):
    def setUp(self):
        signals.post_save.disconnect(model_push, Person)
        self.user = User(username='testuser')
        self.user.save()
        self.person = Person()

    def test_person_needs_user_to_save(self):
        self.assertRaises(TypeError, lambda : self.person.save())
        try:
            self.person.save(self.user)
        except:
            self.fail('The person failed to save with user. Exception:' + str(sys.exc_info()))

    def test_person_model_has_correct_fields(self):
        person = Person()
        for field in Person._meta.fields:
            if field.name in ["first_name", "last_name"]:
                self.assertEqual(isinstance(field, django.db.models.fields.CharField), True)
                self.assertEqual(field.max_length,30)
            if field.name in ["webpage_url", "email_address"]:
                self.assertEqual(isinstance(field, django.db.models.fields.CharField),True)
            if field.name in ["business_phone", "contact_phone"]:
                self.assertEqual(isinstance(field, django.db.models.fields.CharField),True)

    def test_person_string_representation(self):
        first_name = "john"
        last_name = "doe"
        email_address = "jdoe@ufl.edu"
        person = Person(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address
            )

        self.assertEqual(str(person), ' '.join([str(item) for item in [person.first_name, person.last_name, person.email_address]]))
