import json

from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.utils import timezone

from approver.models import Project
from approver.forms import QuestionForm, ProjectForm
from approver.workflows import project_crud
from approver.decorators import login_required
import approver.constants as constants
import approver.utils as utils
from django.core.urlresolvers import reverse

@login_required
def approve(request, project_id=None):
    context = {
        'content': 'approver/approve.html',
        'project_id': project_id,
    }
    current_user = User.objects.get(username=utils.get_current_user_gatorlink(request.session))
    if request.method == 'POST':
        # question_form = request.POST
        # return the route where we build and give the certificate
        # if the whole thing isnt done, still save their answers, maybe kick them back to dash?
        # hit back? ajax answers on lose focus?
        return utils.dashboard_redirect_and_toast(request, 'You posted your questions.')

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
                    # need to be able to prefill this in case people have already
                    # started approving their project but left
                    question_form = QuestionForm()
                    context['sorted_questions'] = question_form.get_sorted_questions()
                    return utils.layout_render(request, context)
        else:
            return utils.dashboard_redirect_and_toast(request, 'You need to have a project.')

