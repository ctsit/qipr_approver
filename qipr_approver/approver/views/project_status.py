import json

from django.contrib.auth.decorators import login_required

from approver.workflows import project_crud
import approver.utils as utils

@login_required
def project_status(request, project_id=None):
    context = {
        'content': 'approver/project_status.html',
        'is_approved': False,
        'need_advisor': False,
    }
    project = project_crud.get_project_or_none(project_id)
    #Returns true if the project needs an associated advisor.
    if (project.get_need_advisor()):
        context['need_advisor'] = True
    # Returns desired project and True if approval was confirmed & time stamped
    if project.approval_date:
        context['is_approved'] = True
        context['project'] = project
    return utils.layout_render(request, context)
