import json

from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from approver.models import Project
from approver.forms import AboutYouForm, ProjectForm
from approver.workflows import project_crud
import approver.constants as constants
import approver.utils as utils

@login_required
def project(request, project_id=None):
    '''Project can be viewed only if it is not archived. SuperUser can edit the archived project'''
    context = {
        'content': 'approver/project.html',
        'project_id': project_id,
        'toast_text': utils.get_and_reset_toast(request.session),
    }
    current_user = request.user
    if request.method == 'POST':
        project_form = request.POST
        title = project_form.get('title')
        project = project_crud.get_project_or_none(project_id)
        if(project is None):
            project = project_crud.create_or_update_project(current_user, project_form, project_id)
            request.access_log.model = project

        else:
            if project.archived and not project_crud.current_user_is_superuser(current_user):
                return utils.dashboard_redirect_and_toast(request, 'Project is Archived.')
            if project_crud.current_user_is_superuser(current_user):
                project = project_crud.create_or_update_project(current_user, project_form, project_id)
                request.access_log.model = project
                return utils.dashboard_su_redirect_and_toast(request, 'Project is Saved.')

            if (project_crud.current_user_is_project_owner(current_user, project) is True and project.get_is_editable() and not project.archived):
                project = project_crud.create_or_update_project(current_user, project_form, project_id)
                request.access_log.model = project
            else:
                return utils.dashboard_redirect_and_toast(request, 'You are not allowed to edit this project'.format(project_id))

        if (not project.title.strip() or not project.description.strip()):
            return utils.project_redirect_and_toast(request, project.id, "Title and Description are required.")

        return redirect(reverse("approver:similar_projects", args=[str(project.id)]))

    else:
        project_form = ProjectForm()
        context['form'] = project_form
        if(project_id is not None):
            project = project_crud.get_project_or_none(project_id)
            if(project is None):
                return utils.dashboard_redirect_and_toast(request, 'Project with id {} does not exist.'.format(project_id))
            else:
                user_can_edit = project_crud.is_current_project_editable_by_user(current_user, project)
                if project_crud.current_user_is_superuser(current_user):
                    context['form'] = ProjectForm(project,is_disabled=not user_can_edit)
                    return utils.layout_render(request,context)

                elif project.archived:
                    toast_message = 'Project is archived.'
                    return utils.dashboard_redirect_and_toast(request, 'Project is Archived.')

                else:
                    context['form'] = ProjectForm(project,is_disabled=not user_can_edit)
                    return utils.layout_render(request,context)
        else:
            #new form
            return utils.layout_render(request, context)
