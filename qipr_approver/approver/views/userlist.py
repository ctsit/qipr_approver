from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render
import approver.utils as utils
from django.contrib.auth.decorators import user_passes_test
from approver.decorators import login_required
from django.http import HttpResponseRedirect
from approver.constants import users_per_page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#@login_required
#@user_passes_test(lambda u: u.is_superuser)
def userlist(request):
	if utils.get_user_from_http_request(request).is_superuser:
		if request.method == 'GET':
			users = []
			userlist = User.objects.all()
			paginator = Paginator(userlist, users_per_page)
			page = request.GET.get('page')
			try:
			        users = paginator.page(page)
			except PageNotAnInteger:
			        users = paginator.page(1)
			except EmptyPage:
			        users = paginator.page(paginator.num_pages)
			context = {
				'content': 'approver/userlist.html',
			    'users': users,
			    'toast_text': utils.get_and_reset_toast(request.session),
			}
			return utils.layout_render(request, context)
		else:
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))