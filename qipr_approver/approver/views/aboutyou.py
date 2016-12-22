from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

from approver.models import Project, Address, Person
from approver.forms import AboutYouForm
from approver.workflows import user_crud

import json
import approver.utils as utils
import approver.constants as constants
from approver.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect

@login_required
def about_you(request):
    context = {
        'content': 'approver/about_you.html',
        'toast_text': utils.get_and_reset_toast(request.session),
        'su_edit':False,
    }
    if request.method == 'POST':
        about_you_form = request.POST
        username = request.session.get(constants.SESSION_VARS['gatorlink'])
        user = User.objects.get(username=username)
        editing_user = User.objects.get(username=utils.get_current_user_gatorlink(request))

        user_crud.update_user_from_about_you_form(user, about_you_form, editing_user)
        return utils.dashboard_redirect_and_toast(request, 'Profile Saved!')

    else:
        username = request.session.get(constants.SESSION_VARS['gatorlink'])
        user = User.objects.get(username=username)
        about_you_form = AboutYouForm(user=user)
        context['form'] = about_you_form
        context['empty_address'] = Address()

    return utils.layout_render(request, context)

#@login_required
#@user_passes_test(lambda u: u.is_superuser)
def about_you_superuser(request,person_id=None):
    '''Super Users should be able to view/change all the user information with 
    About You form. Users that are created through Django Admin and have no person 
    assosiated will not be editable by super user'''
    if not utils.get_user_from_http_request(request).person.is_admin:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'content': 'approver/about_you.html',
        'toast_text': utils.get_and_reset_toast(request.session),
        'su_edit':True,
        'userid':person_id,
    }
    if request.method == 'POST':
        about_you_form = request.POST
        user = Person.objects.get(id=person_id).user
        editing_user = User.objects.get(username=utils.get_current_user_gatorlink(request))
        user_crud.update_user_from_about_you_form(user, about_you_form, editing_user)
        return utils.userlist_su_redirect_and_toast(request,"Profile Saved!")

    else:
        user = Person.objects.get(id=person_id).user
        if hasattr(user,"person") :
            about_you_form = AboutYouForm(user=user)
            context['form'] = about_you_form
            context['empty_address'] = Address()
            return utils.layout_render(request, context)
        else :
            request.session['toast_text'] = 'You donot have permissions to edit this user!'
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

