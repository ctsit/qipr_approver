from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from approver.utils import layout_render

def unsupported_browser(request):
    if request.method == 'GET':
        context = {
            'content': 'approver/unsupported_browser.html',
            'navbar_display': 'none',
            'hide_stats': True,
        }
        return layout_render(request, context)
    elif request.method == 'POST':
        request.session['proceed_anyway'] = True
        return redirect(reverse('approver:index'))

