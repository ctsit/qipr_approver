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
from approver.constants import projects_per_page
from operator import itemgetter

@login_required
def dashboard(request,project_id=None):
    if request.method == 'GET' or request.POST.get('search') is not None:
        search_query = ""
        if(request.POST.get('search') is not None):
            search_query = request.POST.get('search')

        projects = []
        projects_list = sorted(get_project_context(request,search_query),key=itemgetter('last_modified'),reverse=True)
        paginator = Paginator(projects_list, projects_per_page)
        page = request.GET.get('page')
        try:
                projects = paginator.page(page)
        except PageNotAnInteger:
                projects = paginator.page(1)
        except EmptyPage:
                projects = paginator.page(paginator.num_pages)

        user = utils.get_user_from_http_request(request)
        person = user.person
        context = {
            'content': 'approver/dashboard.html',
            'projects': projects,
            'toast_text': utils.get_and_reset_toast(request.session),
            'search_query': search_query,
            'person': person
        }
        return utils.layout_render(request, context)
    elif request.method == 'POST':
        current_user = User.objects.get(username=utils.get_current_user_gatorlink(request.session))
        project = project_crud.get_project_or_none(project_id)
        if(project_id is not None):
            toast_text = project_crud.current_user_can_perform_project_delete(current_user,project)
            return utils.dashboard_redirect_and_toast(request, toast_text)
        else:
            return redirect(reverse("approver:dashboard"))

def get_project_context(request,search_query,super_user=False):
    '''Super Users can view Archived Projects.All the available projects
     will be returned. If not Super User only projects that are not archived will be shown'''
    user = utils.get_user_from_http_request(request)
    if super_user:
        projects = [__get_project_details(project,"Super_User") for project in Project.objects.all().filter(title__icontains=search_query)]
        return projects
    projects = [__get_project_details(project,"PI") for project in user.person.projects.all().filter(title__icontains=search_query).filter(archived=False)]
    collaborator_projects = [__get_project_details(project,"Collaborator") for project in Project.objects.filter(collaborator=user.person).filter(title__icontains=search_query).filter(archived=False)]
    advisor_projects = [__get_project_details(project,"Advisor") for project in Project.objects.filter(advisor=user.person).filter(title__icontains=search_query).filter(archived=False)]
    return projects + collaborator_projects + advisor_projects

def __get_project_details(project, role):
    '''Returns dictionary of all project details that are displayed on Dashboard''' 
    return {'title':project.title,'pk':project.pk,'role':role, 'is_approved':project.is_approved, 'last_modified':project.last_modified,'has_similar_projects':len(project_crud.get_similar_projects(project))}

@login_required
def dashboard_su(request,action=None,project_id=None):
    if not utils.get_user_from_http_request(request).is_superuser:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'GET' or request.POST.get('search') is not None:
        super_user = False
        if utils.get_user_from_http_request(request).is_superuser:
           super_user = True
        search_query = ""
        if(request.POST.get('search') is not None):
            search_query = request.POST.get('search')

        projects = []
        projects_list = sorted(get_project_context(request,search_query,super_user),key=itemgetter('last_modified'),reverse=True)
        paginator = Paginator(projects_list, projects_per_page)
        page = request.GET.get('page')
        try:
                projects = paginator.page(page)
        except PageNotAnInteger:
                projects = paginator.page(1)
        except EmptyPage:
                projects = paginator.page(paginator.num_pages)

        user = utils.get_user_from_http_request(request)
        person = user.person
        context = {
            'content': 'approver/dashboard.html',
            'projects': projects,
            'toast_text': utils.get_and_reset_toast(request.session),
            'search_query': search_query,
            'person': person
        }
        return utils.layout_render(request, context)
    elif request.method == 'POST':
        '''Performs Project Delete and Archive'''
        current_user = User.objects.get(username=utils.get_current_user_gatorlink(request.session))
        project = project_crud.get_project_or_none(project_id)
        if action == 'archive' :
            toast_text = project_crud.current_user_can_perform_project_archive(current_user,project)
            request.session['toast'] = toast_text
            return redirect((reverse("approver:dashboard_su")))
        if(project_id is not None):
            toast_text = project_crud.current_user_can_perform_project_delete(current_user,project)
            request.session['toast'] = toast_text
            return redirect(reverse("approver:dashboard_su"))
        else:
            return redirect(reverse("approver:dashboard_su"))
