from approver.constants import SESSION_VARS, SHIB_ENABLED
from approver import utils

def session_expire(view_function):
    """
    Expires the session, thats it
    """
    def wrapped_view(request, *args, **kwargs):
        request.session.set_expiry(SESSION_VARS['timeout_time'])
        response = view_function(request, *args, **kwargs)
        return response

    return wrapped_view
