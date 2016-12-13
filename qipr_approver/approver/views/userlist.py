from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
import approver.utils as utils
from approver.models import Person
from django.contrib.auth.decorators import user_passes_test
from approver.decorators import login_required
from django.http import HttpResponseRedirect
from approver.constants import users_per_page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#@login_required
#@user_passes_test(lambda u: u.person.is_admin)
def userlist(request):
	if utils.get_user_from_http_request(request).person.is_admin:
		if request.method == 'GET':
			persons_page = []
			person_list = Person.objects.all()
			paginator = Paginator(person_list, users_per_page)
			page = request.GET.get('page')
			try:
			        persons_page = paginator.page(page)
			except PageNotAnInteger:
			        persons_page = paginator.page(1)
			except EmptyPage:
			        persons_page = paginator.page(paginator.num_pages)
			context = {
				'content': 'approver/userlist.html',
			    'persons_page': persons_page,
			    'toast_text': utils.get_and_reset_toast(request.session),
			}
			return utils.layout_render(request, context)
		else:
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
