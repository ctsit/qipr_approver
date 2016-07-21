import json

from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.utils import timezone

from approver.models import Project
from approver.forms import AboutYouForm, ProjectForm
from approver.workflows import project_crud
from approver.decorators import login_required
import approver.constants as constants
import approver.utils as utils
from django.core.urlresolvers import reverse

@login_required
def project(request):
    context = {
        'content': 'approver/project.html',
    }
    if request.method == 'POST':
        project_form = request.POST
        editing_user = User.objects.get(username=utils.get_current_user_gatorlink(request.session))
        title = project_form.get('title')
        if not __project_exists(project_form):
            project = project_crud.create_new_project_from_session_title(request.session, title)
        project_crud.update_project_from_project_form(project, project_form, editing_user)

        saved_form = ProjectForm(initial={'title': project.title,
                                          'description': project.description,
                                          'proposed_start_date': project.proposed_start_date,
                                          'proposed_end_date': project.proposed_end_date})
        request.session['message'] = 'Project Saved!'
        context['form'] = saved_form
        return redirect(reverse("approver:dashboard"))

    else:
        now = timezone.now()
        project_form = ProjectForm(initial={'proposed_start_date': now,'proposed_end_date': now})
        context['form'] = project_form
        if(request.GET.get("project_id")):
            project = Project.objects.get(id=request.GET.get('project_id'))
            project_owner_username = project.owner.user.username
            current_user_username = utils.get_current_user_gatorlink(request.session)
            if project_owner_username != current_user_username:
                request.session['message'] = 'You are not authorized to access this project'
                return redirect(reverse("approver:dashboard"))

            project_form = ProjectForm(initial={'title': project.title, 'description': project.description, 'proposed_start_date': project.proposed_start_date,
                                             'proposed_end_date': project.proposed_end_date, })
            context['form'] = project_form
        return utils.layout_render(request, context)


def __project_exists(project_form):
    """
    This returns a boolean for if the project exists or not
    """
    """still currently broken
    maybe we pass the primary key in the form and if its empty
    then we know the project doesnt exist"""
    return False
