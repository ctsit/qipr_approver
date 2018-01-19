from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import approver.utils as utils
from approver.models import Person
from approver.constants import users_per_page
from django.db.models import Q

@login_required
@user_passes_test(lambda u: u.person.is_admin)
def userlist(request):
    if request.method == 'GET' or request.POST.get('search') is not None:
        persons_page = []
        search_query = ""
        if(request.POST.get('search') is not None):
            search_query = request.POST.get('search')
            person_list = Person.objects.filter(Q(gatorlink__icontains=search_query))
        else:
            person_list = Person.objects.all()
        paginator = Paginator(person_list, users_per_page)
        page = request.GET.get('page')
        if page =='all':
            persons_page = person_list
        else:
            try:
                persons_page = paginator.page(page)
            except PageNotAnInteger:
                persons_page = paginator.page(1)
            except EmptyPage:
                persons_page = paginator.page(paginator.num_pages)
        context = {
                'content': 'approver/userlist.html',
                'persons_page': persons_page,
                'show_all': page == 'all',
                'search_query': search_query,
                'toast_text': utils.get_and_reset_toast(request.session),
            }
        return utils.layout_render(request, context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
