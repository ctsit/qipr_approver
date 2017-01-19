from approver.constants import SESSION_VARS, SHIB_ENABLED
from approver.models import AccessLog
from approver import utils

def log_access(get_response):
    """
    This is a decorator that will log people's access
    and add the previous_log_id to the session for
    easy adjacency stuff
    """
    def middleware(request):
        if __is_logging(request):
            log = __before_view(request)

        response = get_response(request)

        if __is_logging(request):
            __after_view(response, log)

        return response

    return middleware

def __before_view(request):
    """
    Does the logging with the information in the request
    """
    try:
        gatorlink = request.user.person.gatorlink
    except:
        gatorlink = None
    url = request.get_full_path()
    ip = request.META.get('REMOTE_ADDR')
    user_agent_data = request.META.get('HTTP_USER_AGENT')
    user_agent_string = user_agent_data.encode('utf-8') if user_agent_data else 'NONE'.encode('utf-8')
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

def __is_logging(request):
    """
    This function should return true unless there is some reason you dont
    want to log the request. For instance, if requesting the favicon
    """
    is_logging = True

    path = request.get_full_path()
    pieces = path.split('/')

    # dont log static file requests
    if 'static' in pieces:
        is_logging = False

    return is_logging
