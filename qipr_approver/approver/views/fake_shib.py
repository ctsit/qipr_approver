from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect

from approver.workflows import shib

#TODO: implement real shib and get rid of this fake shib endpoint
@csrf_protect
def fake_shib(request):
    if request.method == "GET":
        return render(request, 'approver/fakeshib.html')
    elif request.method == "POST":
        return shib.after_validation(request)
    else:
        raise Http404('This url only supports POST and GET.')
