from approver.models import Speciality, Expertise, QI_Interest, Suffix, ClinicalArea, Self_Classification
from django.contrib.auth.models import User
from approver import utils
class AboutYouForm():

    def __init__(self, user=User()):
        self.first_name = {'name': 'first_name',
                           'placeholder': 'Jane',
                           'label': 'First Name',
                           'type': 'text',
                           'value': user.person.first_name or '',
                           'required': True,
                           'input_classes': 'about__field--box'}

        self.last_name = {'name': 'last_name',
                          'placeholder': 'Doe',
                          'label': 'Last Name',
                          'type': 'text',
                          'required': True,
                          'value': user.person.last_name or '',
                          'input_classes': 'about__field--box'}

        self.title = {'name': 'title',
                      'label': 'Title',
                      'placeholder': 'e.g. Mrs.',
                      'type': 'text',
                      'value': user.person.title or '',
                      'input_classes': 'about__field--box'}

        self.department = {'name': 'department',
                           'placeholder': 'e.g. Pediatrics',
                           'label': 'What is your primary department?',
                           'type': 'text',
                           'value': user.person.department or '',
                           'input_classes': 'about__field--box'}

        self.clinical_area = {'name': 'clinical_area',
                              'placeholder': 'e.g. NICU 2',
                              'label': 'What is your clinical area? Press "enter" to save',
                              'model': 'clinicalarea',
                              'filter_field': 'name',
                              'tag_prop': ClinicalArea.tag_property_name,
                              'options': filter(utils.is_not_none, [item.name for item in ClinicalArea.objects.all()]),
                              'selected': utils.get_related_property(user.person,"clinical_area"),
                              'input_classes': 'about__field--box',
                              'div_classes': 'about__field--width100'}

        self.self_classification = {'name': 'self_classification',
                                    'label': 'Self Classification',
                                    'placeholder': 'Self Classification',
                                    'selected': getattr(user.person.self_classification,'name',''),
                                    'other': user.person.other_self_classification or '',
                                    'tag_prop': Self_Classification.tag_property_name,
                                    'options':  Self_Classification.objects.values_list('name', flat=True).order_by('sort_order'),
                                    'input_class_list': 'about__field-box'}

        self.business_address = user.person.business_address

        self.webpage_url = {'name': 'webpage_url',
                            'placeholder': 'Enter dept webpage url here',
                            'label': 'Webpage URL',
                            'type': 'text',
                            'value': user.person.webpage_url or '',
                            'input_classes': 'about__field--box'}

        self.email = {'name': 'email',
                      'placeholder': 'janedoe@shands.ufl.edu',
                      'label': 'Email Address',
                      'type': 'email',
                      'value': user.person.email_address or '',
                      'input_classes': 'about__field--box'}

        self.business_phone = {'name': 'business_phone',
                               'placeholder': '(555) 555-5555',
                               'label': 'Business Phone Number',
                               'type': 'text',
                               'value': user.person.business_phone or '',
                               'input_classes': 'about__field--box'}

        self.contact_phone = {'name': 'contact_phone',
                              'placeholder': '(555) 555-5555',
                              'label': 'Contact Phone Number',
                              'type': 'text',
                              'value': user.person.contact_phone or '',
                              'input_classes': 'about__field--box'}

        self.speciality_tags = {'name': 'speciality',
                                'placeholder': 'e.g. Pediatric Nephrology',
                                'label': 'What is your speciality or certification? Press "enter" to save.',
                                'model': 'speciality',
                                'tag_prop': Speciality.tag_property_name,
                                'filter_field': 'name',
                                'options': [item.name for item in Speciality.objects.all()],
                                'selected': [item.name for item in user.person.speciality.all()],
                                'input_classes': 'about__field--box, about__details--height',
                                'div_classes': 'about__field--width100'}

        self.qi_interest_tags = {'name': 'qi_interest',
                                 'placeholder': 'e.g. Transitions in Care',
                                 'label': 'List your Quality Improvement Interests. Press "enter" to save.',
                                 'model': 'qi_interest',
                                 'filter_field': 'name',
                                 'tag_prop': QI_Interest.tag_property_name,
                                 'options': [item.name for item in QI_Interest.objects.all()],
                                 'selected': [item.name for item in user.person.qi_interest.all()],
                                 'input_classes': 'about__field--box',
                                 'div_classes': 'about__field--width100'}

        self.expertise_tags = {'name': 'expertise',
                               'placeholder': 'e.g. Nephrotic Syndrome',
                               'label': 'What is your area of expertise? Press "enter" to save.',
                               'model': 'expertise',
                               'filter_field': 'name',
                               'tag_prop': Expertise.tag_property_name,
                               'options': [item.name for item in Expertise.objects.all()],
                               'selected': [item.name for item in user.person.expertise.all()],
                               'input_classes': 'about__field--box',
                               'div_classes': 'about__field--width100'}

        self.suffix_tags = {'name': 'suffix',
                            'label': 'Degree/Suffix',
                            'placeholder': 'e.g. PhD or M.D.',
                            'model': 'suffix',
                            'filter_field': 'name',
                            'tag_prop': Suffix.tag_property_name,
                            'options': [item.name for item in Suffix.objects.all()],
                            'selected': [item.name for item in user.person.suffix.all()],
                            'input_classes': 'about__field--box',
                            'div_classes': 'about__field--width100'}

        self.qi_required = user.person.qi_required

        self.last_login = {'name': 'last_login',
                           'label': 'Last Login',
                           'type': 'text',
                           'value': user.person.last_login_time or '',
                           'input_classes': 'about__acctinfo--border',
                           'div_classes': 'about__acctinfo'}

        self.account_expiration = {'name': 'account_expiration',
                           'label': 'Account Expiration',
                           'type': 'text',
                           'value': user.person.account_expiration_time or '',
                           'input_classes': 'about__acctinfo--border',
                           'div_classes': 'about__acctinfo'}

        self.account_created = {'name': 'account_created',
                           'label': 'Account Created',
                           'type': 'text',
                           'value': user.date_joined or '',
                           'input_classes': 'about__acctinfo--border',
                           'div_classes': 'about__acctinfo'}

        self.training_program = {'name': 'training_program',
                           'label': 'Training Program',
                           'placeholder': 'If you selected yes, enter your training program here.',
                           'type': 'text',
                           'value': user.person.training or '',
                           'input_classes': 'about__field--box',
                           'div_classes': 'about__question--train'}

