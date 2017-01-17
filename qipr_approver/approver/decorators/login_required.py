from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings

from approver.constants import SESSION_VARS

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
        """
        Shibboleth places a token in the HTTP_EPPN meta data key to prove
        it has authenticated properly. So, if SHIB is enabled, and has this
        key, it is assumed validated. If SHIB is not enabled, this doesn't
        matter.
        """
        return ((settings.SHIB_ENABLED and request.META.get('HTTP_EPPN')) or not settings.SHIB_ENABLED)

    return wrapped_view
