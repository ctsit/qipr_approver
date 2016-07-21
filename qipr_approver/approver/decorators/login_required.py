from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from approver.constants import SESSION_VARS

def login_required(view_function):
    """
    This is a decorator that will redirect people to shib if
    they do not have a user in their session.
    """
    def wrapped_view(request):
        if request.session.get(SESSION_VARS.get('gatorlink')):
            return view_function(request)
        else:
            return redirect(reverse("approver:shib"))
    return wrapped_view
