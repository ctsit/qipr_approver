from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
import approver.utils as utils


def error404(request):
    context = {
        'content': 'approver/404.html',
    }
    return utils.layout_render(request,context)