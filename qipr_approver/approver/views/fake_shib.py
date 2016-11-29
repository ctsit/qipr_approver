from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect

from approver.workflows import shib
from approver.constants import SHIB_ENABLED

#TODO: implement real shib and get rid of this fake shib endpoint
@csrf_protect
def fake_shib(request):
    if SHIB_ENABLED == 'false':
        if request.method == "GET":
            return render(request, 'approver/fakeshib.html')
        elif request.method == "POST":
            return shib.after_validation(request)
        else:
            raise Http404('This url only supports POST and GET.')

    else:
        if (request.META.get('HTTP_EPPN') and SHIB_ENABLED == 'true'):
            return shib.after_validation(request)
        else:
            raise Http404('There is a problem with your Shibboleth django settings')
