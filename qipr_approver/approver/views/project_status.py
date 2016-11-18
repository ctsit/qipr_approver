import json

from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.utils import timezone

from approver.models import Project
from approver.workflows import project_crud
from approver.decorators import login_required
import approver.constants as constants
import approver.utils as utils
from django.core.urlresolvers import reverse

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
