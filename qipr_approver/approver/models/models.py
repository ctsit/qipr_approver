from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from approver.constants import STATE_CHOICES, COUNTRY_CHOICES

from approver import utils

class TaggedWithName(models.Model):
    tag_property_name = 'name'
    class Meta:
        abstract = True

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

    def save(self, last_modified_by, *args, **kwargs):
        utils.set_created_by_if_empty(self, last_modified_by)
        self.audit_trail.user = last_modified_by
        self.last_modified_by = last_modified_by
        super(Provenance, self).save(*args, **kwargs)

    def delete(self, last_modified_by, *args, **kwargs):
        self.audit_trail.user = last_modified_by
        self.last_modified_by = last_modified_by
        super(Provenance, self).delete(*args, **kwargs)


    class Meta:
        abstract = True

class Training(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=200)

class Organization(Provenance):
    org_name = models.CharField(max_length= 400)

    def __str__(self):
        return self.org_name

class Speciality(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class Position(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class Keyword(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class SafetyTarget(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class ClinicalArea(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class ClinicalSetting(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class Suffix(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

class Expertise(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class QI_Interest(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class Category(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

class BigAim(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=100)
    sort_order = models.IntegerField()

class FocusArea(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=100)
    sort_order = models.IntegerField()

class ClinicalDepartment(Provenance, NamePrint, TaggedWithName):
    name = models.CharField(max_length=100)
    sort_order = models.IntegerField()

class Person(Provenance):
    user = models.OneToOneField(User, null=True, related_name="person")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    position = models.ManyToManyField(Position)
    account_expiration_time = models.DateTimeField(null=True)
    business_phone = models.CharField(max_length=50, null=True)
    contact_phone = models.CharField(max_length=50, null=True)
    email_address = models.CharField(max_length=100, null=True)
    expertise = models.ManyToManyField(Expertise)
    first_name = models.CharField(max_length=30)
    last_login_time = models.DateTimeField(null=True)
    last_name = models.CharField(max_length=30)
    organization = models.ManyToManyField(Organization)
    position = models.ManyToManyField(Position)
    qi_interest = models.ManyToManyField(QI_Interest)
    speciality = models.ManyToManyField(Speciality)
    suffix = models.ManyToManyField(Suffix)
    training = models.ManyToManyField(Training)
    user = models.OneToOneField(User, null=True, related_name="person")
    webpage_url = models.CharField(max_length=50, null=True)

    tag_property_name = 'email_address'

    def __str__(self):
        return ' '.join([self.first_name, self.last_name, self.email_address])


class Project(Provenance):
    advisor = models.ManyToManyField(Person, related_name="advised_projects")
    approval_date = models.DateTimeField(null=True)
    big_aim = models.ManyToManyField(BigAim)
    description = models.TextField()
    category = models.ManyToManyField(Category)
    clinical_area = models.ManyToManyField(ClinicalArea)
    clinical_setting = models.ManyToManyField(ClinicalSetting)
    collaborator = models.ManyToManyField(Person, related_name="collaborations")
    keyword = models.ManyToManyField(Keyword)
    owner = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL, related_name="projects")
    proposed_end_date = models.DateTimeField(null=True)
    proposed_start_date = models.DateTimeField(null=True)
    safety_target = models.ManyToManyField(SafetyTarget)
    title = models.CharField(max_length=300)

    def __str__(self):
        return ' '.join([self.title, str(self.owner)])

    def get_is_editable(self):
        """
        Returns true if the project is editable.
        Projects get locked down after they are approved
        or a year after their creation date.
        """
        """right now this is broken"""
        timeelapsed = timezone.now() - self.created
        if timeelapsed.seconds > 31536000 or self.approval_date :
            return False
        return True

    def approve(self, user):
        self.approval_date = timezone.now()
        self.save(user)

class Address(Provenance):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, related_name="business_address")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name="org_address")
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, null=True, blank=True)

    def __str__(self):
        return ' ; '.join([self.address1,
                           self.address2,
                           self.city,
                           self.zip_code,
                           self.state,
                           self.country])

