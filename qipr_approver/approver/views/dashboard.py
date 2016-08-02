from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from approver.forms import AboutYouForm, ProjectForm
from django.contrib.auth.models import User
from approver.models import Person
from approver.models import Project

import json
import approver.utils as utils
import approver.constants as constants
from approver.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from itertools import chain

@login_required
def dashboard(request):
    project_title = []
    projects = []
    context = {
        'content': 'approver/dashboard.html',
        'projects' : get_project_context(request),
        'toast_text' : utils.get_and_reset_toast(request.session)
    }

    return utils.layout_render(request, context)

def get_project_context(request):
    username = request.session.get(constants.SESSION_VARS['gatorlink'])
    user = User.objects.get(username=username)
    projects = user.person.projects.all()
    collaborator_projects = Project.objects.filter(collaborator=user.person)
    advisor_projects = Project.objects.filter(advisor=user.person)
    return [__get_project_tuples(project) for project in chain(projects,collaborator_projects,advisor_projects)]

def __get_project_tuples(project):
    return (project.title,
            project.pk)
