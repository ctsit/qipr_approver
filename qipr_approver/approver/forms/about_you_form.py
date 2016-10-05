from approver.models import Speciality, Expertise, QI_Interest, Suffix, ClinicalArea
from django.contrib.auth.models import User
from approver import utils
class AboutYouForm():

    def __init__(self, user=User()):
        self.user_name = {'name': 'user_name',
                          'label': 'Gatorlink',
                          'type': 'text',
                          'value': user.username or ''}

        self.first_name = {'name': 'first_name',
                           'placeholder': 'Jane',
                           'label': 'First Name',
                           'type': 'text',
                           'value': user.person.first_name or ''}

        self.last_name = {'name': 'last_name',
                          'placeholder': 'Doe',
                          'label': 'Last Name',
                          'type': 'text',
                          'value': user.person.last_name or ''}

        self.title = {'name': 'title',
                      'label': 'Tite',
                      'type': 'text',
                      'value': user.person.title or ''}

        self.department = {'name': 'department',
                           'label': 'Department',
                           'type': 'text',
                           'value': user.person.department or ''}

        self.clinical_area = {'name': 'clinical_area',
                              'label': 'Clinical Area',
                              'options': filter(utils.is_not_none, [item.name for item in ClinicalArea.objects.all()]),
                              'selected': utils.get_related_property(user.person,"clinical_area")}

        self.business_address = user.person.business_address

        self.webpage_url = {'name': 'webpage_url',
                            'label': 'Webpage URL',
                            'type': 'text',
                            'value': user.person.webpage_url or ''}

        self.email = {'name': 'email',
                      'placeholder': 'janedoe@ufl.edu',
                      'label': 'Email Address',
                      'type': 'email',
                      'value': user.email or ''}

        self.business_phone = {'name': 'business_phone',
                               'placeholder': '(555) 555-5555',
                               'label': 'Business Phone Number',
                               'type': 'text',
                               'value': user.person.business_phone or ''}

        self.contact_phone = {'name': 'contact_phone',
                              'placeholder': '(555) 555-5555',
                              'label': 'Contact Phone Number',
                              'type': 'text',
                              'value': user.person.contact_phone or ''}

        self.speciality_tags = {'name': 'speciality',
                                'label': 'Speciality',
                                'options': [item.name for item in Speciality.objects.all()],
                                'selected': [item.name for item in user.person.speciality.all()]}

        self.qi_interest_tags = {'name': 'qi_interest',
                                 'label': 'Quality Improvement Interests',
                                 'options': [item.name for item in QI_Interest.objects.all()],
                                 'selected': [item.name for item in user.person.qi_interest.all()]}

        self.expertise_tags = {'name': 'expertise',
                               'label': 'Expertise',
                               'options': [item.name for item in Expertise.objects.all()],
                               'selected': [item.name for item in user.person.expertise.all()]}

        self.suffix_tags = {'name': 'suffix',
                            'label': 'Suffix',
                            'options': [item.name for item in Suffix.objects.all()],
                            'selected': [item.name for item in user.person.suffix.all()]}

        self.qi_required = user.person.qi_required 

        self.last_login = {'name': 'last_login',
                           'label': 'Last Login',
                           'type': 'text',
                           'value': user.person.last_login_time or ''}

        self.account_expiration = {'name': 'account_expiration',
                           'label': 'Account Expiration',
                           'type': 'text',
                           'value': user.person.account_expiration_time or ''}

        self.account_created = {'name': 'account_created',
                           'label': 'Account Created',
                           'type': 'text',
                           'value': user.date_joined or ''}
