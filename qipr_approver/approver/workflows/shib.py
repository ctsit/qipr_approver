from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from approver.models import Person
from approver.constants import SESSION_VARS
from . import user_crud

def add_shib_information_to_session(request):
    """
    This function takes the information we have received from shib
    and places it inside the session.
    """
    """This will need to be changed when we get shib hooked up
    TODO:set expiry and other sessiony things"""
    request.session[SESSION_VARS['gatorlink']] = request.POST.get('gatorlink')
    request.session[SESSION_VARS['email']] = request.POST.get('gatorlink') + '@ufl.edu'
    request.session[SESSION_VARS['first_name']] = 'FAKE FIRST NAME'
    request.session[SESSION_VARS['last_name']] = 'FAKE LAST NAME'

def after_validation(request):
    """This function is to be called with what shib sends us"""
    """
    Note that this will need to be changed when the real shib gets hooked up.
    Wont be adding cleartext cookie stuff, apache will hijack the
    requests and add thigns to the header which is where we will pull
    the gatorlink from
    """
    gatorlink = request.POST.get('gatorlink')
    add_shib_information_to_session(request)
    if len(User.objects.filter(username=gatorlink)) == 0:
        new_user = user_crud.create_new_user_from_current_session(request.session)
        response = redirect(reverse("approver:aboutyou"))
        return response
    else:
        return redirect(reverse("approver:dashboard"))

