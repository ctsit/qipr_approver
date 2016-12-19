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
                             'placeholder': 'Type collaborator name, then click "enter" to save',
                             'filter_field': 'email_address',
                             'options': filter(utils.is_not_none, [item.email_address for item in Person.objects.all()]),
                             'selected': utils.get_related_property(project, "collaborator", 'email_address')}

        self.advisor = {'name': 'advisor',
                        'model': 'person',
                        'placeholder': 'Type advisor name, then click "enter" to save',
                        'filter_field': 'email_address',
                        'options': filter(utils.is_not_none, [item.email_address for item in Person.objects.all()]),
                        'selected': utils.get_related_property(project, "advisor", 'email_address')}

        self.mesh_keyword = {'name': 'mesh_keyword',
                        'label': 'MeSH Keywords',
                        'options': filter(utils.is_not_none, [item.mesh_heading for item in Descriptor.objects.all()]),
                        'selected': utils.get_related_property(project, "mesh_keyword")}

        self.keyword = {'name': 'keyword',
                        'label': 'Keywords',
                        'model': 'keyword',
                        'placeholder': 'Type keyword, then click "enter" to save',
                        'filter_field': 'name',
                        'options': filter(utils.is_not_none, [item.name for item in Keyword.objects.all()]),
                        'selected': utils.get_related_property(project, "keyword"),
                        'div_classes': 'about__txtfield--100'}

        self.big_aim = {'name': 'big_aim',
                        'label': 'UF Health Big Aims',
                        'model': 'bigaim',
                        'placeholder': 'Type big aim, then click "enter" to save',
                        'filter_field': 'name',
                        'options': filter(utils.is_not_none, [item.name for item in BigAim.objects.all()]),
                        'selected': utils.get_related_property(project, "big_aim"),
                        'div_classes': 'about__txtfield--100'}

        self.clinical_area = {'name': 'clinical_area',
                              'label': 'Clinical Area/Unit',
                              'options': filter(utils.is_not_none, [item.name for item in ClinicalArea.objects.all()]),
                              'selected': utils.get_related_property(project,"clinical_area"),
                              'model': 'clinicalarea',
                              'placeholder': 'Type clinical area, then click "enter" to save',
                              'filter_field': 'name',
                              'options': filter(utils.is_not_none, [item.name for item in ClinicalArea.objects.all()]),
                              'selected': utils.get_related_property(project,"clinical_area"),
                              'div_classes': 'about__txtfield--100'}

        self.clinical_setting = {'name': 'clinical_setting',
                                 'label': 'Clinical Setting',
                                 'model': 'clinicalsetting',
                                 'placeholder': 'Type clinical setting, then click "enter" to save',
                                 'filter_field': 'name',
                                 'options': filter(utils.is_not_none, [item.name for item in ClinicalSetting.objects.all()]),
                                 'selected': utils.get_related_property(project,"clinical_setting"),
                                 'div_classes': 'about__txtfield--100'}

        self.description = {'name': 'description',
                            'type': 'text',
                            
                            'input_classes': ['description__height'], 
                            'placeholder': 'Give a brief description about your Quality Improvement project (up to 250 words)',
                            'value': project.description or ''}

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
