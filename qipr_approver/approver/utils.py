from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

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

def get_and_reset_toast(session):
    toast = session.get("toast_text")
    session['toast_text'] = ''
    return toast

def dashboard_redirect_and_toast(request, toast_text):
    request.session['toast_text'] = toast_text
    return redirect(reverse("approver:dashboard"))

def set_created_by_if_empty(model, user):
    """
    This function is called by our save function because django
    throws exceptions on object access if something doesn't exist.
    You cannot dereference a related field if it doesn't exist.
    Meaning you have to do a try except block.
    """
    try:
        # the following line throws an exception
        model.created_by is not None
    except:
        model.created_by = user

def format_date(date):
    date_parts = [date.year, date.month, date.day]
    return '/'.join([str(part) for part in date_parts])
