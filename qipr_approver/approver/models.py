from django.db import models
from django.contrib.auth.models import User
from approver.constants import STATE_CHOICES, COUNTRY_CHOICES

from approver import utils

class NamePrint(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Provenance(models.Model):
    created_by = models.ForeignKey(User,editable=False,related_name="+")
    last_modified_by = models.ForeignKey(User,related_name="+")
    created = models.DateTimeField(auto_now_add=True,editable=False)
    last_modified = models.DateTimeField(auto_now=True,editable=True)

    def after_create(self, user):
        self.created_by = user
        self.last_modified_by = user

    def save(self, last_modified_by, *args, **kwargs):
        self.last_modified_by = last_modified_by
        super(Provenance, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Training(Provenance, NamePrint):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

class Address(Provenance):
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField(null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, null=True, blank=True)

    def __str__(self):
        return ' ; '.join([self.address1,
                           self.address2,
                           self.city,
                           self.zip_code,
                           self.state,
                           self.country])

class Organization(Provenance):
    org_name = models.CharField(max_length= 400)
    address = models.ManyToManyField(Address)

    def __str__(self):
        return self.org_name

class Speciality(Provenance, NamePrint):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class Position(Provenance, NamePrint):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class Keyword(Provenance, NamePrint):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class SafetyTarget(Provenance, NamePrint):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class ClinicalArea(Provenance, NamePrint):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class ClinicalSetting(Provenance, NamePrint):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class Suffix(Provenance, NamePrint):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

class Expertise(Provenance, NamePrint):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class QI_Interests(Provenance, NamePrint):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class Category(Provenance, NamePrint):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class Section(Provenance, NamePrint):
    name = models.CharField(max_length=30)
    sort_order = models.IntegerField(unique=True)

class Question(Provenance):
    section = models.ForeignKey(Section)
    text = models.TextField()
    sort_order = models.IntegerField()

class Choice(Provenance):
    question = models.ForeignKey(Question)
    text = models.TextField()
    sort_order = models.IntegerField()

class Person(Provenance):
    user = models.OneToOneField(User,related_name="person")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    position = models.ManyToManyField(Position)
    organization = models.ManyToManyField(Organization)
    business_address = models.ManyToManyField(Address)
    business_phone = models.IntegerField(null=True)
    contact_phone = models.IntegerField(null=True)
    email_address = models.CharField(max_length=100, null=True)
    speciality = models.ManyToManyField(Speciality)
    training = models.ManyToManyField(Training)
    webpage_url = models.CharField(max_length=50, null=True)
    suffix = models.ManyToManyField(Suffix)
    expertise = models.ManyToManyField(Expertise)
    qi_interests = models.ManyToManyField(QI_Interests)
    last_login_time = models.DateTimeField(null=True)
    account_expiration_time = models.DateTimeField(null=True)

    def __str__(self):
        return ' '.join([self.first_name, self.last_name, self.email_address])


class Project(Provenance):
    title = models.CharField(max_length=300)
    description = models.TextField()
    owner = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL, related_name="projects")
    keywords = models.ManyToManyField(Keyword)
    category = models.ManyToManyField(Category)
    collaborators = models.ManyToManyField(Person, related_name="collaborations")
    advisor = models.ManyToManyField(Person, related_name="advised_projects")
    proposed_start_date = models.DateTimeField(null=True)
    proposed_end_date = models.DateTimeField(null=True)
    safety_targets = models.ManyToManyField(SafetyTarget)
    clinical_area = models.ManyToManyField(ClinicalArea)
    clinic_setting = models.ManyToManyField(ClinicalSetting)

    def __str__(self):
        return ' '.join([self.title, self.owner])

class Response(Provenance):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    choice = models.ForeignKey(Choice)
    project = models.ForeignKey(Project)
    free_text_response = models.TextField()
