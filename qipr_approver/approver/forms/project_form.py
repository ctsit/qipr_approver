from django.utils import timezone
from approver.models import Project
from approver import utils

class ProjectForm():

    def __init__(self, project=Project()):
        start_date = project.proposed_start_date or timezone.now()
        end_date = project.proposed_end_date or timezone.now()
        self.title = {'name': 'title',
                      'label': 'Title',
                      'type': 'text',
                      'value': project.title or ''}

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
