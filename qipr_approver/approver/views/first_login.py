from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from approver.forms import AboutYouForm, ProjectForm
from django.contrib.auth.models import User
from approver.models import Project

import json
import approver.utils as utils
import approver.constants as constants

def first_login(request):
    context = {
        'content': 'approver/first_login.html',
    }
    return utils.layout_render(request,context)
