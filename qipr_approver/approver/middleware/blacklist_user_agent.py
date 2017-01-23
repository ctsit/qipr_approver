from django.shortcuts import render

from approver.constants import SESSION_VARS, SHIB_ENABLED
from approver.models import AccessLog
from approver import utils
from approver import constants
from approver.views import unsupported_browser

def blacklist_user_agent(get_response):
    """
    This is a decorator that will log people's access
    and add the previous_log_id to the session for
    easy adjacency stuff
    """
    def middleware(request):

        if __is_valid(request):
            response = get_response(request)
        elif request.session.get('proceed_anyway') == True:
            response = get_response(request)
        else:
            response = unsupported_browser(request)

        return response

    return middleware

def __is_valid(request):
    user_agent = request.META.get('HTTP_USER_AGENT') or ''

    valid_ua = __is_valid_user_agent(user_agent, constants.bad_user_agent_strings)
    is_static_request = __is_static_request(request)

    return valid_ua or is_static_request

def __is_valid_user_agent(user_agent, bad_agents):
    for bad_text in bad_agents:
        if bad_text in user_agent:
            return False
        else:
            pass
    return True

def __is_static_request(request):
    steps = request.path.split('/')
    return ('static' in steps)
