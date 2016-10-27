import json

from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.utils import timezone

from approver.models import Project
from approver.forms import QuestionForm, ProjectForm
from approver.workflows import project_crud, approve_workflow
from approver.decorators import login_required
import approver.constants as constants
import approver.utils as utils
from django.core.urlresolvers import reverse

@login_required
def approve(request, project_id=None):
    context = {
        'content': 'approver/approve.html',
        'project_id': project_id,
        'toast_text': utils.get_and_reset_toast(request.session)
    }
    current_user = User.objects.get(username=utils.get_current_user_gatorlink(request.session))
    if request.method == 'POST':
        question_form = request.POST
        project = project_crud.get_project_or_none(project_id)
        approve_workflow.save_project_with_form(project, question_form, request.session)
        return approve_workflow.approve_or_next_steps(project, current_user)

    else:
        now = timezone.now()
        if(project_id is not None):
            project = project_crud.get_project_or_none(project_id)
            if(project is None):
                return utils.dashboard_redirect_and_toast(request, 'Project with id {} does not exist.'.format(project_id))
            else:
                if(project_crud.curent_user_is_project_owner(current_user, project) is not True
                   or project.get_is_editable() is not True):
                    return utils.dashboard_redirect_and_toast(request, 'You are not authorized to edit this project.')
                else:
                    question_form = QuestionForm(project_id=project_id)
                    context['sorted_questions'] = question_form.get_random_questions()

                    return utils.layout_render(request, context)
        else:
            return utils.dashboard_redirect_and_toast(request, 'You need to have a project.')

