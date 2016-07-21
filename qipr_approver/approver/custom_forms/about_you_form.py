from approver.models import Speciality

class AboutYouForm():

    def __init__(self, user):
        self.user_name = {'name': 'user_name',
                          'label': 'Gatorlink',
                          'type': 'text',
                          'html_id': 'user_' + str(user.pk),
                          'value': user.username}

        self.first_name = {'name': 'first_name',
                           'label': 'First Name',
                           'type': 'text',
                           'html_id': 'first_name_' + str(user.pk),
                           'value': user.person.first_name}

        self.last_name = {'name': 'last_name',
                          'label': 'Last Name',
                          'type': 'text',
                          'html_id': 'last_name_' + str(user.pk),
                          'value': user.person.last_name}

        self.webpage_url = {'name': 'webpage_url',
                            'label': 'Webpage URL',
                            'type': 'text',
                            'html_id': 'webpage_url_' + str(user.pk),
                            'value': user.person.webpage_url}

        self.email = {'name': 'email',
                      'label': 'Email Address',
                      'type': 'email',
                      'html_id': 'email_' + str(user.pk),
                      'value': user.email}

        self.business_phone = {'name': 'business_phone',
                               'label': 'Business Phone Number',
                               'type': 'text',
                               'html_id': 'business_phone_' + str(user.pk),
                               'value': user.person.business_phone}

        self.contact_phone = {'name': 'contact_phone',
                              'label': 'Contact Phone Number',
                              'type': 'text',
                              'html_id': 'contact_phone_' + str(user.pk),
                              'value': user.person.contact_phone}

        self.speciality_tags = {'name': 'speciality',
                                'label': 'Speciality',
                                'options': [item.name for item in Speciality.objects.all()],
                                'selected': ['progaming']}

