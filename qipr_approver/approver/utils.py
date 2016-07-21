from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

import datetime

import approver.constants as constants

def user_exists(about_you_form):
    """
    Returns True if user exists, and False otherwise given an
    about_you_form
    """
    return (len(User.objects.filter(username=about_you_form.get('user_name'))) != 0)

def layout_render(request, context):
    """
    This function should be used in place of render.
    It adds context['content'] into the layout.html so that the nav bar is
    present as well as css and javascript
    """
    return render(request, 'approver/layout.html', context)

def get_current_user_gatorlink(session):
    """
    Gets the current user's gatorlink
    We don't return the user here because the util file shall
    not have a dependency on the models
    """
    return session.get(constants.SESSION_VARS['gatorlink'])

def get_and_reset_message(session):
    message = session.get("message")
    session['message'] = ''
    return message