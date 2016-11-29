from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect

from approver.workflows import shib
from approver.constants import SHIB_ENABLED

@csrf_protect
def shib_login(request):
    """
    If Shibboleth is enabled on this server, a request
    should go right through and processed in the workflow.
    If not, the login page should be displayed (GET) and
    processed through the workflow when submitted (POST)
    """
    if SHIB_ENABLED == 'true':
        if (request.META.get('HTTP_EPPN')):
            return shib.after_validation(request)
        else:
            raise Http404('There is a problem with your Shibboleth django settings')
    else:
        if request.method == "GET":
            return render(request, 'approver/shib.html')
        elif request.method == "POST":
            return shib.after_validation(request)
        else:
            raise Http404('This url only supports POST and GET.')
