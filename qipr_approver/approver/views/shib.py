from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

from approver.workflows import shib

@csrf_protect
def shib_login(request):
    """
    If Shibboleth is enabled on this server, a request
    should go right through and processed in the workflow.
    If not, the login page should be displayed (GET) and
    processed through the workflow when submitted (POST)
    """
    new_person = request.session.pop('IS_NEW_PERSON',False)
    if settings.SHIB_ENABLED:
        if new_person:
            #This is a new person, they should visit the about you page first
            return redirect(reverse("approver:aboutyou"))
        else:
            #This person is not new and should go to the dashboard
            return redirect(reverse("approver:dashboard"))
    else:
        if request.method == "GET":
            return render(request, 'approver/shib.html')
        elif request.method == "POST":
            return shib.after_validation(request)
        else:
            raise Http404('This url only supports POST and GET.')
