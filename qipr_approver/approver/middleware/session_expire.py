from approver.constants import SESSION_VARS, SHIB_ENABLED
from approver import utils

def session_expire(get_response):
    """
    Expires the session, thats it
    """
    def middleware(request):
        request.session.set_expiry(SESSION_VARS['timeout_time'])
        return get_response(request)

    return middleware
