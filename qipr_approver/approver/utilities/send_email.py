import smtplib
from email.message import EmailMessage

from django.conf import settings
from django.core.mail import send_mail

def send_email(subject, message_body, from_email, to_emails):
    '''
    Create an email message using pythons smtplib and EmailMessage.
    It returns a dictionary, with one entry for each recipient that was
    refused. Each entry contains a tuple of the SMTP error code and the
    accompanying error message sent by the server.

    Args:
    subject: a string for the subject line
    message_body: a string for the email message body
    from_email: who the email is coming from
    to_emails: either a string or list of emails address being sent to
    '''
    if settings.DEBUG:
        return send_mail(subject,message_body,from_email, __get_list(to_emails))

    msg = __create_message(subject, message_body, from_email, to_emails)
    return __send(msg)

def __connect_to_smtp():
    '''
    Using Django settings and smtplib, create an smtplib SMTP instance
    https://docs.python.org/3/library/smtplib.html#smtplib.SMTP
    '''
    connection = smtplib.SMTP(host=settings.QIPR_EMAIL_HOST,
                              port=settings.QIPR_EMAIL_PORT,
                              local_hostname=settings.QIPR_EMAIL_HOSTNAME)
    return connection

def __send(message):
    connection = __connect_to_smtp()
    failures = connection.send_message(message)
    connection.quit()
    return failures

def __create_message(subject, message_body, from_email, to_emails):
    '''
    Take the subject, message body, from email, and to emails list and create
    a message object to send off.
    '''
    msg = EmailMessage()
    msg.set_content(message_body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = __get_list(to_emails)
    return msg

def __get_list(string_or_list):
    '''
    Take a string and return a list
    '''
    if isinstance(string_or_list, list):
        return string_or_list
    try:
        return string_or_list.split()
    except AttributeError:
        return []
