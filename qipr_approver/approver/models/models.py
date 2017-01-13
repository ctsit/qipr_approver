from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from approver.constants import STATE_CHOICES, COUNTRY_CHOICES, QI_CHECK

from approver import utils
from approver import constants
from approver.models.bridge_models import Registerable
from approver.models.tag_models import Tag, TagPrint, TaggedWithName

class Provenance(models.Model):
    created_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, related_name="+")
    last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True, editable=True)
    guid = models.CharField(max_length=32, default=utils.get_guid, editable=False)

    def save(self, last_modified_by, *args, **kwargs):
        utils.set_created_by_if_empty(self, last_modified_by)
        try:
            self.audit_trail.user = last_modified_by
        except:
            pass
        utils.set_guid_if_empty(self)
        self.last_modified_by = last_modified_by
        super(Provenance, self).save(*args, **kwargs)

    def delete(self, last_modified_by, *args, **kwargs):
        try:
            self.audit_trail.user = last_modified_by
        except:
            pass
        self.last_modified_by = last_modified_by
        super(Provenance, self).delete(*args, **kwargs)

    class Meta:
        abstract = True

class DataList(Registerable):
    name = models.CharField(max_length=400)
    description = models.CharField(max_length=400, null=True)
    sort_order = models.IntegerField(null=True)

    def __str__(self, delimiter=' '):
        return delimiter.join([self.name, self.description or ''])

    def get_natural_dict(self):
        return {
            'name': str(self.name),
            'description': str(self.description),
        }

    class Meta:
        abstract = True


class Organization(Provenance, Registerable):
    org_name = models.CharField(max_length= 400)

    def __str__(self, delimiter=' '):
        return self.org_name

class Training(Provenance, TagPrint, TaggedWithName, Registerable):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True)

class BigAim(Provenance, DataList):
    pass
class Category(Provenance, Tag):
    pass
class ClinicalArea(Provenance, Tag):
    pass
class ClinicalSetting(Provenance, Tag):
    pass
class Expertise(Provenance, Tag):
    pass
class Keyword(Provenance, Tag):
    pass
class Position(Provenance, Tag):
    pass
class QI_Interest(Provenance, Tag):
    pass
class Self_Classification(Provenance, DataList):
    pass
class Speciality(Provenance, Tag):
    pass
class Suffix(Provenance, Tag):
    pass

class FocusArea(Provenance, Tag):
    sort_order = models.IntegerField(null=True)
class ClinicalDepartment(Provenance, Tag):
    sort_order = models.IntegerField(null=True)

class Person(Provenance, Registerable):
    account_expiration_time = models.DateTimeField(null=True)
    business_phone = models.CharField(max_length=50, null=True)
    contact_phone = models.CharField(max_length=50, null=True)
    email_address = models.CharField(max_length=100, null=True)
    expertise = models.ManyToManyField(Expertise)
    first_name = models.CharField(max_length=30)
    gatorlink = models.CharField(max_length=50, null=True)
    last_login_time = models.DateTimeField(null=True)
    last_name = models.CharField(max_length=30)
    organization = models.ManyToManyField(Organization)
    position = models.ManyToManyField(Position)
    qi_interest = models.ManyToManyField(QI_Interest)
    speciality = models.ManyToManyField(Speciality)
    suffix = models.ManyToManyField(Suffix)
    training = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name="person")
    webpage_url = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
    department = models.CharField(max_length=50, null=True)
    qi_required = models.SmallIntegerField(null=True)
    clinical_area = models.ManyToManyField(ClinicalArea)
    self_classification = models.ForeignKey(Self_Classification, null=True, on_delete=models.SET_NULL,
                                            related_name="person")
    other_self_classification = models.CharField(max_length=100, null=True)
    tag_property_name = 'email_address'
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ', ' + self.last_name + ' (' + self.email_address + ')'

    def get_natural_dict(self):
        return {
            'gatorlink': self.gatorlink,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email_address': self.email_address,
            'model_class_name': self.__class__.__name__,
        }


class Project(Provenance, Registerable):
    advisor = models.ManyToManyField(Person, related_name="advised_projects")
    approval_date = models.DateTimeField(null=True)
    big_aim = models.ForeignKey(BigAim, null=True, on_delete=models.SET_NULL, related_name="projects")
    category = models.ManyToManyField(Category)
    clinical_area = models.ManyToManyField(ClinicalArea)
    clinical_setting = models.ManyToManyField(ClinicalSetting)
    collaborator = models.ManyToManyField(Person, related_name="collaborations")
    description = models.TextField()
    objective = models.TextField()
    scope = models.TextField()
    measures = models.TextField()
    milestones = models.TextField()
    keyword = models.ManyToManyField(Keyword)
    owner = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL, related_name="projects")
    proposed_end_date = models.DateTimeField(null=True)
    proposed_start_date = models.DateTimeField(null=True)
    title = models.CharField(max_length=300)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return ' '.join([self.title, str(self.owner.gatorlink)])

    def get_is_editable(self):
        """
        Returns true if the project is editable.
        Projects get locked down after they are approved
        or a year after their creation date.
        """
        if utils.check_is_date_past_year(self.created) or self.approval_date:
            return False
        return True

    def is_approved(self):
        return self.approval_date or self.in_registry

    def approve(self, user):
        self.approval_date = timezone.now()
        self.save(user)

    def get_natural_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'owner': self.owner.natural_key(),
            'collaborators': [item.natural_key() for item in self.collaborator.all()],
            'keyword': [item.natural_key() for item in self.keyword.all()],
            'model_class_name': self.__class__.__name__,
        }

    def get_need_advisor(self):
        """
        Determine if the project needs an advisor based on whether qi is a requirement for the owner.
        """
        return self.owner.qi_required == QI_CHECK['yes'] and len(self.advisor.all()) == 0

class Address(Provenance, Registerable):
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

    def get_natural_dict(self):
        return {
            'address1': self.address1,
            'address2': self.address2,
            'city': self.city,
            'zip_code': self.zip_code,
            'state': self.state,
            'country': self.country,
            'person': self.person.natural_key(),
        }
