from approver.models import Speciality, Expertise, QI_Interest, Suffix
from django.contrib.auth.models import User

class AboutYouForm():

    def __init__(self, user=User()):
        self.user_name = {'name': 'user_name',
                          'label': 'Gatorlink',
                          'type': 'text',
                          'value': user.username or ''}

        self.first_name = {'name': 'first_name',
                           'label': 'First Name',
                           'type': 'text',
                           'value': user.person.first_name or ''}

        self.last_name = {'name': 'last_name',
                          'label': 'Last Name',
                          'type': 'text',
                          'value': user.person.last_name or ''}

        self.business_address = user.person.business_address

        self.webpage_url = {'name': 'webpage_url',
                            'label': 'Webpage URL',
                            'type': 'text',
                            'value': user.person.webpage_url or ''}

        self.email = {'name': 'email',
                      'label': 'Email Address',
                      'type': 'email',
                      'value': user.email or ''}

        self.business_phone = {'name': 'business_phone',
                               'label': 'Business Phone Number',
                               'type': 'text',
                               'value': user.person.business_phone or ''}

        self.contact_phone = {'name': 'contact_phone',
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

