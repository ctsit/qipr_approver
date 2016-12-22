from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from approver.constants import SESSION_VARS, SHIB_ENABLED
from . import user_crud
from approver import utils

def add_shib_information_to_session(request):
    """
    This function takes the information we have received from shib
    and places it inside the session.
    """
    request.session[SESSION_VARS['gatorlink']] = __get_gatorlink_from_request(request)
    request.session[SESSION_VARS['email']] = __get_email_from_request(request)
    request.session[SESSION_VARS['first_name']] = request.META.get('HTTP_GIVENNAME') or ''
    request.session[SESSION_VARS['last_name']] = request.META.get('HTTP_SN') or ''

def after_validation(request):
    """This function is to be called with what shib sends us"""

    gatorlink = __get_gatorlink_from_request(request)
    add_shib_information_to_session(request)
    if len(User.objects.filter(username=gatorlink)) == 0:
        new_user = user_crud.create_new_user_from_current_session(request.session)
        response = redirect(reverse("approver:aboutyou"))
        return response
    else:
        user = User.objects.get(username=gatorlink)
        user.person.last_login_time = timezone.now()
        user.person.account_expiration_time=utils.get_account_expiration_date(timezone.now())
        user.person.save(user)
        request.session['su'] = user.person.is_admin
        return redirect(reverse("approver:dashboard"))

def __get_email_from_request(request):
    if utils.shib_enabled():
        return request.META.get('HTTP_MAIL')
    else:
        return request.POST.get('gatorlink') + '@ufl.edu'

def __get_gatorlink_from_request(request):
    if utils.shib_enabled():
        return request.META.get('HTTP_GLID')
    else:
        return request.POST.get('gatorlink')
