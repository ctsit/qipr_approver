from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings

class DebugShibMiddleware(object):
    """
    This Middleware simply injects some fake
    Shibboleth-like variables into the request Metadata.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        if not settings.DEBUG:
            raise MiddlewareNotUsed

    def __call__(self, request):
        #add fake shib variables here
        request.META['REMOTE_USER'] = 'kbarber@ufl.edu'
        request.META['HTTP_GLID'] = 'kbarber'
        request.META['HTTP_MAIL'] = 'kbarber@ufl.edu'
        request.META['HTTP_GIVENNAME'] = 'Kate'
        request.META['HTTP_SN'] = 'Barber'
        request.META['HTTP_POSTALADDRESS'] = 'PO BOX 100219$GAINESVILLE$FL$326100219'
        response = self.get_response(request)
        return response
