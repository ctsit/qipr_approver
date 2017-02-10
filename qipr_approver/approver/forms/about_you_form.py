from approver.models import Speciality, Expertise, QI_Interest, Suffix, ClinicalArea, Self_Classification, ClinicalDepartment
from django.contrib.auth.models import User
from approver import utils
class AboutYouForm():

    def __init__(self, user=None, person=None):
        person = person if person else user.person
        date_joined = user.date_joined if user else None

        self.first_name = {'name': 'first_name',
                           'placeholder': 'Jane',
                           'label': 'First Name',
                           'type': 'text',
                           'value': person.first_name or '',
                           'required': True,
                           'input_classes': 'about__field--box'}

        self.last_name = {'name': 'last_name',
                          'placeholder': 'Doe',
                          'label': 'Last Name',
                          'type': 'text',
                          'required': True,
                          'value': person.last_name or '',
                          'input_classes': 'about__field--box'}

        self.title = {'name': 'title',
                      'label': 'Title',
                      'placeholder': 'e.g. Mrs.',
                      'type': 'text',
                      'value': person.title or '',
                      'input_classes': 'about__field--box'}

        self.department = {'name': 'department',
                           'placeholder': 'Department',
                           'label': 'What is your primary department?',
                           'selected': getattr(person.department,'name',''),
                           'options': ClinicalDepartment.objects.values_list('name', flat=True).order_by('sort_order'),
                           'input_classes': 'about__field--box'}

        self.clinical_area = {'name': 'clinical_area',
                              'placeholder': 'e.g. NICU 2',
                              'label': 'What is your clinical area? Press "enter" to save',
                              'model': 'clinicalarea',
                              'filter_field': 'name',
                              'selected': utils.get_related(person,"clinical_area"),
                              'input_classes': 'about__field--box',
                              'div_classes': 'about__field--width100'}

        self.self_classification = {'name': 'self_classification',
                                    'label': 'Self Classification',
                                    'placeholder': 'Self Classification',
                                    'selected': getattr(person.self_classification,'name',''),
                                    'other': person.other_self_classification or '',
                                    'options':  Self_Classification.objects.values_list('name', flat=True).order_by('sort_order'),
                                    'input_class_list': 'about__field-box'}

        self.business_address = person.business_address

        self.webpage_url = {'name': 'webpage_url',
                            'placeholder': 'Enter dept webpage url here',
                            'label': 'Webpage URL',
                            'type': 'text',
                            'value': person.webpage_url or '',
                            'input_classes': 'about__field--box'}

        self.email = {'name': 'email',
                      'placeholder': 'janedoe@shands.ufl.edu',
                      'label': 'Email Address',
                      'type': 'email',
                      'value': person.email_address or '',
                      'input_classes': 'about__field--box'}

        self.business_phone = {'name': 'business_phone',
                               'placeholder': '(555) 555-5555',
                               'label': 'Business Phone Number',
                               'type': 'text',
                               'value': person.business_phone or '',
                               'input_classes': 'about__field--box'}

        self.contact_phone = {'name': 'contact_phone',
                              'placeholder': '(555) 555-5555',
                              'label': 'Contact Phone Number',
                              'type': 'text',
                              'value': person.contact_phone or '',
                              'input_classes': 'about__field--box'}

        self.speciality_tags = {'name': 'speciality',
                                'placeholder': 'e.g. Pediatric Nephrology',
                                'label': 'What is your speciality or certification? Press "enter" to save.',
                                'model': 'speciality',
                                'filter_field': 'name',
                                'selected': utils.get_related(person, 'speciality'),
                                'input_classes': 'about__field--box, about__details--height',
                                'div_classes': 'about__field--width100'}

        self.qi_interest_tags = {'name': 'qi_interest',
                                 'placeholder': 'e.g. Transitions in Care',
                                 'label': 'List your Quality Improvement Interests. Press "enter" to save.',
                                 'model': 'qi_interest',
                                 'filter_field': 'name',
                                 'selected': utils.get_related(person, 'qi_interest'),
                                 'input_classes': 'about__field--box',
                                 'div_classes': 'about__field--width100'}

        self.expertise_tags = {'name': 'expertise',
                               'placeholder': 'e.g. Nephrotic Syndrome',
                               'label': 'What is your area of expertise? Press "enter" to save.',
                               'model': 'descriptor',
                               'filter_field': 'mesh_heading',
                               'selected': utils.get_related(person, 'expertise'),
                               'input_classes': 'about__field--box',
                               'div_classes': 'about__field--width100'}

        self.suffix_tags = {'name': 'suffix',
                            'label': 'Degree/Suffix',
                            'placeholder': 'e.g. PhD or M.D.',
                            'model': 'suffix',
                            'filter_field': 'name',
                            'selected':  utils.get_related(person, 'suffix'),
                            'input_classes': 'about__field--box',
                            'div_classes': 'about__field--width100'}

        self.qi_required = person.qi_required

        self.last_login = {'name': 'last_login',
                           'label': 'Last Login',
                           'type': 'text',
                           'value': person.last_login_time or '',
                           'input_classes': 'about__acctinfo--border',
                           'div_classes': 'about__acctinfo'}

        self.account_expiration = {'name': 'account_expiration',
                           'label': 'Account Expiration',
                           'type': 'text',
                           'value': person.account_expiration_time or '',
                           'input_classes': 'about__acctinfo--border',
                           'div_classes': 'about__acctinfo'}

        self.account_created = {'name': 'account_created',
                           'label': 'Account Created',
                           'type': 'text',
                           'value': date_joined or '',
                           'input_classes': 'about__acctinfo--border',
                           'div_classes': 'about__acctinfo'}

        self.training_program = {'name': 'training_program',
                           'label': 'Training Program',
                           'placeholder': 'If you selected yes, enter your training program here.',
                           'type': 'text',
                           'value': person.training or '',
                           'input_classes': 'about__field--box',
                           'div_classes': 'about__question--train'}

