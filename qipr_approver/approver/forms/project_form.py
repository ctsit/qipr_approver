from django.utils import timezone
from approver.models import Project, Keyword, ClinicalArea, ClinicalSetting, SafetyTarget, Person, BigAim
from django.contrib.auth.models import User
from approver import utils

class ProjectForm():

    def __init__(self, project=Project(),is_disabled=False):
        start_date = project.proposed_start_date or timezone.now()
        end_date = project.proposed_end_date or timezone.now()

        self.is_disabled = is_disabled

        self.title = {'name': 'title',
                      'label': 'Title',
                      'type': 'text',
                      'rows': 2,
                      'value': project.title or ''}

        self.collaborator = {'name': 'collaborator',
                             'label': 'Collaborators',
                             'options': filter(utils.is_not_none, [item.email_address for item in Person.objects.all()]),
                             'selected': utils.get_related_property(project, "collaborator", 'email_address')}

        self.advisor = {'name': 'advisor',
                        'label': 'Advisors',
                        'options': filter(utils.is_not_none, [item.email_address for item in Person.objects.all()]),
                        'selected': utils.get_related_property(project, "advisor", 'email_address')}

        self.keyword = {'name': 'keyword',
                        'label': 'Keywords',
                        'options': filter(utils.is_not_none, [item.name for item in Keyword.objects.all()]),
                        'selected': utils.get_related_property(project, "keyword")}

        self.big_aim = {'name': 'big_aim',
                        'label': 'Big Aims',
                        'options': filter(utils.is_not_none, [item.name for item in BigAim.objects.all()]),
                        'selected': utils.get_related_property(project, "big_aim")}

        self.clinical_area = {'name': 'clinical_area',
                               'label': 'Clinical Area/Unit',
                               'options': filter(utils.is_not_none, [item.name for item in ClinicalArea.objects.all()]),
                               'selected': utils.get_related_property(project,"clinical_area")}

        self.safety_target = {'name': 'safety_target',
                               'label': 'Safety Targets',
                               'options': filter(utils.is_not_none, [item.name for item in SafetyTarget.objects.all()]),
                               'selected': utils.get_related_property(project,"safety_target")}

        self.clinical_setting = {'name': 'clinical_setting',
                                 'label': 'Clinical Setting',
                                 'options': filter(utils.is_not_none, [item.name for item in ClinicalSetting.objects.all()]),
                                 'selected': utils.get_related_property(project,"clinical_setting")}

        self.description = {'name': 'description',
                            'label': 'Description',
                            'type': 'text',
                            'rows': 3,
                            'value': project.description or ''}

        self.proposed_start_date = {'name': 'proposed_start_date',
                                    'input_classes': ['datepicker'],
                                    'label': 'Proposed Start Date',
                                    'type': 'date',
                                    'value': utils.format_date(start_date)}

        self.proposed_end_date = {'name': 'proposed_end_date',
                                  'input_classes': ['datepicker'],
                                   'label': 'Proposed End Date',
                                   'type': 'date',
                                   'value': utils.format_date(end_date)}
