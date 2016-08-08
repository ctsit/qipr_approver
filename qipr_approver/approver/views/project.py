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
def project(request, project_id=None):
    context = {
        'content': 'approver/project.html',
        'project_id': project_id,
    }
    current_user = User.objects.get(username=utils.get_current_user_gatorlink(request.session))
    if request.method == 'POST':
        project_form = request.POST
        title = project_form.get('title')
        project = project_crud.create_or_update_project(current_user, project_form, project_id)
        return redirect(reverse("approver:approve") + str(project.id) + '/')

    else:
        now = timezone.now()
        project_form = ProjectForm()
        context['form'] = project_form
        if(project_id is not None):
            project = project_crud.get_project_or_none(project_id)
            if(project is None):
                return utils.dashboard_redirect_and_toast(request, 'Project with id {} does not exist.'.format(project_id))
            else:
                if(project_crud.curent_user_is_project_owner(current_user, project) is not True):
                    if project_crud.current_user_is_project_advisor_or_collaborator(current_user,project):
                        context['form'] = ProjectForm(project,is_disabled=True)
                        return utils.layout_render(request,context)
                    else:
                        return utils.dashboard_redirect_and_toast(request, 'You are not authorized to edit this project.')
                else:
                    if (project.get_is_editable() is not True):
                        context['form'] = ProjectForm(project,is_disabled=True)
                        return utils.layout_render(request,context)
                    else:
                        context['form'] = ProjectForm(project)
                        return utils.layout_render(request, context)
        else:
            return utils.layout_render(request, context)
