from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from approver.constants import SESSION_VARS, SHIB_ENABLED

def login_required(view_function):
    """
    This is a decorator that will redirect people to shib if
    they do not have a user in their session.
    """
    def wrapped_view(request, *args, **kwargs):
        if request.session.get(SESSION_VARS.get('gatorlink')):
            if __shib_validated(request):
                return view_function(request, *args, **kwargs)
        return redirect(reverse("approver:shib"))

    def __shib_validated(request):
        return ((SHIB_ENABLED == 'true' and request.META.get('HTTP_EPPN')) or (SHIB_ENABLED == 'false'))

    return wrapped_view
