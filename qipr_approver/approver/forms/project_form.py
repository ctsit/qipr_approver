from django.utils import timezone
from approver.models import Project,Keyword,ClinicalArea,ClinicalSetting,SafetyTarget
from django.contrib.auth.models import User
from approver import utils

class ProjectForm():

    def __init__(self, project=Project()):
        start_date = project.proposed_start_date or timezone.now()
        end_date = project.proposed_end_date or timezone.now()
        self.title = {'name': 'title',
                      'label': 'Title',
                      'type': 'text',
                      'value': project.title or ''}

        self.keyword = {'name': 'keyword',
                         'label': 'Keywords',
                         'options': [item.name for item in Keyword.objects.all()],
                         'selected': utils.get_related_or_empty(project,"keyword")}
        
        self.clinical_area = {'name': 'clinical_area',
                               'label': 'Clinical Area',
                               'options': [item.name for item in ClinicalArea.objects.all()],
                               'selected': utils.get_related_or_empty(project,"clinical_area")}

        self.safety_target = {'name': 'safety_target',
                               'label': 'Safety Targets',
                               'options': [item.name for item in SafetyTarget.objects.all()],
                               'selected': utils.get_related_or_empty(project,"safety_target")}

        self.clinical_setting = {'name': 'clinical_setting',
                                 'label': 'Clinical Setting',
                                 'options': [item.name for item in ClinicalSetting.objects.all()],
                                 'selected': utils.get_related_or_empty(project,"clinical_setting")}
        
        self.description = {'name': 'description',
                            'label': 'Description',
                            'type': 'text',
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
    
    #Get Data from Project for the given field
    def get_related_or_empty(self,modelname,field): 
      return [item.name for item in getattr(modelname,field).all()] if getattr(modelname,'title') else []
