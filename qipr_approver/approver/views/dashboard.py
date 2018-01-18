import json
from operator import itemgetter

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q

from approver.forms import AboutYouForm, ProjectForm
from approver.models import Person
from approver.models import Project
from approver.workflows import project_crud
from approver.constants import projects_per_page

import approver.utils as utils
import approver.constants as constants

@login_required
def dashboard(request,project_id=None):
    if request.method == 'GET' or request.POST.get('search') is not None:
        return __shared_GET(request, project_id)

    elif request.method == 'POST':
        current_user = request.user
        project = project_crud.get_project_or_none(project_id)
        if(project_id is not None):
            toast_text = project_crud.current_user_can_perform_project_delete(current_user,project)
            return utils.dashboard_redirect_and_toast(request, toast_text)
        else:
            return redirect(reverse("approver:dashboard"))


@login_required
@user_passes_test(lambda u: u.person.is_admin)
def dashboard_su(request,action=None,project_id=None):
    active_person = request.user.person

    if request.method == 'GET' or request.POST.get('search') is not None:
        super_user = active_person.is_admin
        return __shared_GET(request, project_id, super_user)

    elif request.method == 'POST':
        '''Performs Project Delete and Archive'''
        current_user = request.user
        project = project_crud.get_project_or_none(project_id)
        if action == 'archive' and project_id is not None:
            toast_text = project_crud.current_user_can_archive_project(current_user,project)
            return utils.dashboard_su_redirect_and_toast(request, toast_text)
        if action == 'unarchive' and project_id is not None:
            toast_text = project_crud.current_user_can_unarchive_project(current_user,project)
            return utils.dashboard_su_redirect_and_toast(request, toast_text)
        if action == 'delete' and project_id is not None :
            toast_text = project_crud.current_user_can_perform_project_delete(current_user,project)
            return utils.dashboard_su_redirect_and_toast(request, toast_text)
        else:
            return redirect(reverse("approver:dashboard_su"))

def __shared_GET(request, project_id, super_user=None):
    search_query = ""
    if(request.POST.get('search') is not None):
        search_query = request.POST.get('search')

    projects = []
    if super_user:
        projects_list = sorted(get_project_context(request,search_query,super_user),key=itemgetter('last_modified'),reverse=True)
    else:
        projects_list = sorted(get_project_context(request,search_query),key=itemgetter('last_modified'),reverse=True)

    paginator = Paginator(projects_list, projects_per_page)
    page = request.GET.get('page')
    try:
        if page == 'all':
            projects = projects_list
        else:
            projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    person = request.user.person
    context = {
        'content': 'approver/dashboard.html' if not super_user else 'approver/dashboard_su.html',
        'projects': projects,
        'toast_text': utils.get_and_reset_toast(request.session),
        'search_query': search_query,
        'show_all': page == 'all',
        'person': person
    }
    return utils.layout_render(request, context)

def get_project_context(request,search_query,super_user=False):
    '''Super Users can view Archived Projects.All the available projects
     will be returned. If not Super User only projects that are not archived will be shown'''
    user = request.user
    if super_user:
        projects = [__get_project_details(project,"Super_User") for project in Project.objects.all().select_related('owner').filter(Q(title__icontains=search_query) | Q(owner__gatorlink__icontains=search_query))]
        return projects
    projects = [__get_project_details(project,"QPI") for project in user.person.projects.all().filter(title__icontains=search_query).filter(archived=False)]
    collaborator_projects = [__get_project_details(project,"Collaborator") for project in Project.objects.filter(collaborator=user.person).filter(title__icontains=search_query).filter(archived=False)]
    advisor_projects = [__get_project_details(project,"Advisor") for project in Project.objects.filter(advisor=user.person).filter(title__icontains=search_query).filter(archived=False)]
    return projects + collaborator_projects + advisor_projects

def __get_project_details(project, role):
    '''Returns dictionary of all project details that are displayed on Dashboard''' 
    return {'title':project.title,
            'pk':project.pk,
            'role':role,
            'is_approved':project.is_approved,
            'last_modified':project.last_modified,
            'is_archived':project.archived,
            'owner': getattr(project.owner,'gatorlink','None')
           }
