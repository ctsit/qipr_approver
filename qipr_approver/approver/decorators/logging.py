from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from approver.constants import SESSION_VARS, SHIB_ENABLED
from approver.models import AccessLog
from approver import utils

def log_access(view_function):
    """
    This is a decorator that will log people's access
    and add the previous_log_id to the session for
    easy adjacency stuff
    """
    def wrapped_view(request, *args, **kwargs):
        request.session.set_expiry(SESSION_VARS['timeout_time'])
        log = __before_view(request, *args, **kwargs)

        response = view_function(request, *args, **kwargs)

        __after_view(response, log)

        return response

    return wrapped_view

def __before_view(request, *args, **kwargs):
    """
    Does the logging with the information in the request
    """
    try:
        gatorlink = utils.get_current_user_gatorlink(request)
    except:
        gatorlink = None
    url = request.get_full_path()
    ip = request.META.get('REMOTE_ADDR')
    user_agent_string = request.META.get('HTTP_USER_AGENT').encode('utf-8')
    http_verb = request.method
    request_body = request.body

    log = AccessLog(gatorlink=gatorlink,
                    ip=ip,
                    url=url,
                    http_verb=http_verb,
                    request_body=request_body)

    log.add_user_agent(user_agent_string)
    __update_log_previous(log, request)
    log.save()
    __update_session_previous(log, request)

    return log

def __update_log_previous(log, request):
    """
    Updates the log to have the right previous value from the session
    """
    prev_id = request.session.get(SESSION_VARS.get('previous_log_id'))
    if prev_id:
        if type(prev_id) == type('string'):
            prev_id = int(prev_id)
        try:
            prev_log = AccessLog.objects.get(id=prev_id)
            log.previous_log = prev_log
        except:
            pass

def __update_session_previous(log, request):
    """
    Updates the session to have the value of the log passed
    """
    request.session[SESSION_VARS['previous_log_id']] = log.id

def __after_view(response, log):
    """
    Logs stuff about the response
    """
    log.response_code = response.status_code
    log.reason_phrase = response.reason_phrase
    log.save()

