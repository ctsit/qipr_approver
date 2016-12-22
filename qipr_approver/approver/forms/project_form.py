from django.utils import timezone
from approver.models import Project, Keyword, ClinicalArea, ClinicalSetting, Person, BigAim, Descriptor
from django.contrib.auth.models import User
from approver import utils

class ProjectForm():

    def __init__(self, project=Project(),is_disabled=False):
        start_date = project.proposed_start_date or timezone.now()
        end_date = project.proposed_end_date or timezone.now()

        self.is_disabled = is_disabled

        self.title = {'name': 'title',
                      'type': 'text',
                      'rows': 2,
                      'placeholder': 'Full project title goes here',
                      'value': project.title or ''}

        self.collaborator = {'name': 'collaborator',
                             'model': 'person',
                             'placeholder': 'e.g. Alligator, Albert',
                             'label': 'Type collaborator name, then press "enter" to save',
                             'filter_field': 'email_address',
                             'options': filter(utils.is_not_none, [item.email_address for item in Person.objects.all()]),
                             'selected': utils.get_related_property(project, "collaborator", 'email_address')}

        self.advisor = {'name': 'advisor',
                        'model': 'person',
                        'placeholder': 'e.g. Alligator, Alberta',
                        'label': 'Type advisor name, then press "enter" to save',
                        'filter_field': 'email_address',
                        'options': filter(utils.is_not_none, [item.email_address for item in Person.objects.all()]),
                        'selected': utils.get_related_property(project, "advisor", 'email_address')}

        self.mesh_keyword = {'name': 'mesh_keyword',
                             'label': 'MeSH Keywords',
                             'model': 'descriptor',
                             'filter_field': 'mesh_heading',
                             'options': filter(utils.is_not_none, [item.mesh_heading for item in Descriptor.objects.all()]),
                             'selected': utils.get_related_property(project, "mesh_keyword", "mesh_heading")}

        self.keyword = {'name': 'keyword',
                        'label': 'Keywords',
                        'model': 'keyword',
                        'placeholder': 'e.g. Micronutrient and/or Zinc',
                        'label': 'Please indicate 5 or more keywords relating to your project. Type keyword, then press "enter" to save',
                        'filter_field': 'name',
                        'options': filter(utils.is_not_none, [item.name for item in Keyword.objects.all()]),
                        'selected': utils.get_related_property(project, "keyword"),
                        'div_classes': 'about__txtfield--100'}

        self.big_aim = {'name': 'big_aim',
                        'label': 'Please indicate the UF Health Big Aims relating to your project. Type keyword, then press "enter" to save',
                        'model': 'bigaim',
                        'placeholder': 'e.g. Zero Harm and/or Increase Value',
                        'filter_field': 'name',
                        'options': filter(utils.is_not_none, [item.name for item in BigAim.objects.all()]),
                        'selected': utils.get_related_property(project, "big_aim"),
                        'div_classes': 'about__txtfield--100'}

        self.clinical_area = {'name': 'clinical_area',
                              'label': 'OPTIONAL: What is the Clinical Area/Unit of your project? Type clinical area, then press "enter" to save',
                              'options': filter(utils.is_not_none, [item.name for item in ClinicalArea.objects.all()]),
                              'selected': utils.get_related_property(project,"clinical_area"),
                              'model': 'clinicalarea',
                              'placeholder': 'e.g. NICU 3 and/or Unit 64',
                              'filter_field': 'name',
                              'options': filter(utils.is_not_none, [item.name for item in ClinicalArea.objects.all()]),
                              'selected': utils.get_related_property(project,"clinical_area"),
                              'div_classes': 'about__txtfield--100'}

        self.clinical_setting = {'name': 'clinical_setting',
                                 'label': 'What is the Clinical Setting of your project? Type clinical setting, then press "enter" to save',
                                 'model': 'clinicalsetting',
                                 'placeholder': 'e.g. NICU and/or General Medicine.',
                                 'filter_field': 'name',
                                 'options': filter(utils.is_not_none, [item.name for item in ClinicalSetting.objects.all()]),
                                 'selected': utils.get_related_property(project,"clinical_setting"),
                                 'div_classes': 'about__txtfield--100'}

        self.description = {'name': 'description',
                            'type': 'text',
                            'input_classes': ['description__height'],
                            'placeholder': 'Give a description of your Quality Improvement project here (Please use at least 250 words. When filled, this input box holds roughly 250 words.)',
                            'value': project.description or ''}

        self.objective = {'name': 'objective',
                          'type': 'text',
                          'input_classes': ['textarea__height'],
                          'placeholder': 'Give a brief description about your Quality Improvement project\'s objectives (up to 250 words)',
                          'value': project.objective or ''}

        self.scope = {'name': 'scope',
                      'type': 'text',
                      'input_classes': ['textarea__height'],
                      'placeholder': 'Give a brief description about your Quality Improvement project\'s scope (up to 250 words)',
                      'value': project.scope or ''}

        self.measures = {'name': 'measures',
                         'type': 'text',
                         'input_classes': ['textarea__height'],
                         'placeholder': 'Give a brief description about your Quality Improvement project\'s measures (up to 250 words)',
                         'value': project.measures or ''}

        self.milestones = {'name': 'milestones',
                           'type': 'text',
                           'input_classes': ['textarea__height'],
                           'placeholder': 'Give a brief description about your Quality Improvement project\'s milestones (up to 250 words)',
                           'value': project.milestones or ''}

        self.proposed_start_date = {'name': 'proposed_start_date',
                                    'input_classes': ['datepicker'],
                                    'label': 'Proposed Start Date',
                                    'type': 'date',
                                    'value': utils.format_date(start_date),
                                    'div_classes': 'about__txtfield--date'}

        self.proposed_end_date = {'name': 'proposed_end_date',
                                  'input_classes': ['datepicker'],
                                   'label': 'Proposed End Date',
                                   'type': 'date',
                                   'value': utils.format_date(end_date),
                                   'div_classes': 'about__txtfield--date'}
