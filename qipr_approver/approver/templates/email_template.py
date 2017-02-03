'''
This is a template for any emails this application will send.
Things in braces should be left alone as they are populated
dynamically
'''

def get_email_body_person_added(first_name, last_name, role,
                                project_title, project_url):
    kwargs = {
        'first_name':first_name,
        'last_name': last_name,
        'role': role,
        'project_title': project_title,
    }

    body_string = '{first_name} {last_name} has listed you as ' + __a_or_an(role) + \
                  ' {role} for the qulatiy improvement project titled: ' \
                  '"{project_title}." \n\n' + __project_url(project_url) + \
                  '\n\n' + __email_footer()

    return body_string.format(**kwargs)

def get_email_subject_person_added():
    return 'You have been added to a quality improvement project'

def get_email_sent_confirmation_body(project_title, project_url):
    kwargs = {
    }
    body = 'This email is to alert you that your quality improvement project titled: ' \
           '"{project_title}" has been saved. \n' + \
           'All collaborators and advisors have been alerted \n\n' + \
            __project_url(project_url) + '\n\n' + __email_footer()

    return body.format(project_title=project_title)

def get_email_subject_confirmation():
    return 'Your quality improvement project has been saved'

def __email_footer():
    return 'Please contact the Quality office with any questions or issues.'

def __project_url(project_url):
    return 'You may view this project at this link: ' + project_url

def __a_or_an(phrase):
    if phrase[0].lower() in 'aeiou':
        return 'an'
    return 'a'
