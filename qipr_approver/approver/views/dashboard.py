from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from approver.forms import AboutYouForm, ProjectForm
from django.contrib.auth.models import User
from approver.models import Person
from approver.models import Project
from approver.workflows import project_crud
from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
import json
import approver.utils as utils
import approver.constants as constants
from approver.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone

@login_required
def dashboard(request,project_id=None):
    if request.method == 'GET':
        project_title = []
        projects = []
        context = {
            'content': 'approver/dashboard.html',
            'projects': get_project_context(request),
            'toast_text': utils.get_and_reset_toast(request.session)
        }
        return utils.layout_render(request, context)
    elif request.method == 'POST':
        current_user = User.objects.get(username=utils.get_current_user_gatorlink(request.session))
        project = project_crud.get_project_or_none(project_id)
        if(project_id is not None):
            toast_text = project_crud.current_user_can_perform_project_delete(current_user,project)
            if(toast_text == 'Deleted Project'):
                return redirect(reverse("approver:dashboard"))
            else:
                return utils.dashboard_redirect_and_toast(request, toast_text)
        else:
            return redirect(reverse("approver:dashboard"))

def get_project_context(request):
    username = request.session.get(constants.SESSION_VARS['gatorlink'])
    user = User.objects.get(username=username)
    projects = [__get_project_tuples(project,"PI") for project in user.person.projects.all()]
    collaborator_projects = [__get_project_tuples(project,"Collaborator") for project in Project.objects.filter(collaborator=user.person)]
    advisor_projects = [__get_project_tuples(project,"Advisor") for project in Project.objects.filter(advisor=user.person)]
    return projects + collaborator_projects + advisor_projects

def __get_project_tuples(project, role):
    return (project.title,
            project.pk,role)
