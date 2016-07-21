from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from approver.forms import AboutYouForm, ProjectForm
from django.contrib.auth.models import User
from approver.models import Person
from approver.models import Project

import json
import approver.utils as utils
import approver.constants as constants
from approver.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

@login_required
def dashboard(request):
	project_title = []
	projects = []
	if request.method == 'GET':
		username = request.session.get(constants.SESSION_VARS['gatorlink'])
		if(len(User.objects.filter(username=username)) != 0):
			user = User.objects.get(username=username)
			if(len(Person.objects.filter(user_id=user.id)) != 0):
				person = Person.objects.get(user_id=user.id)
				projects_list = person.projects.all()
				paginator = Paginator(projects_list, 1) # Show 25 contacts per page
				page = request.GET.get('page')
			try:
				projects = paginator.page(page)
			except PageNotAnInteger:
				projects = paginator.page(1)
			except EmptyPage:      
				projects = paginator.page(paginator.num_pages)

				context = {
					'content': 'approver/dashboard.html',
					'projects' : projects,
					'toast_text' : utils.get_and_reset_message(request.session)
				}
				return utils.layout_render(request, context)
				#project_title = [project.title for project in projects]
	context = {
		'content': 'approver/dashboard.html',
		'projects' : projects,
		'toast_text' : utils.get_and_reset_message(request.session)
	}
	return utils.layout_render(request, context)
