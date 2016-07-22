from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

from approver.models import Project
from approver.forms import AboutYouForm
from approver.workflows import user_crud

import json
import approver.utils as utils
import approver.constants as constants
from approver.decorators import login_required

@login_required
def about_you(request):
    context = {
        'content': 'approver/about_you.html',
        'toast_text': None,
    }
    if request.method == 'POST':
        about_you_form = request.POST
        user = User.objects.get(username=about_you_form.get('user_name'))
        editing_user = User.objects.get(username=utils.get_current_user_gatorlink(request.session))

        user_crud.update_user_from_about_you_form(user, about_you_form, editing_user)
        return utils.dashboard_redirect_and_toast(request, 'Profile Saved!')

    else:
        username = request.session.get(constants.SESSION_VARS['gatorlink'])
        user = User.objects.get(username=username)
        about_you_form = AboutYouForm(user=user)
        context['form'] = about_you_form

    return utils.layout_render(request, context)

