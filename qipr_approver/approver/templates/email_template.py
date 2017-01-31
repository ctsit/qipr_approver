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
        'project_url': project_url,
    }

    body_string = '{first_name} {last_name} has listed you as ' + __a_or_an(role) + \
                  ' {role} for the qulatiy improvement project titled: ' \
                  '"{project_title}." \n\n' \
                  'You may view this project at this link: {project_url} \n\n' \
                  'Please contact the Quality office with any questions or issues.'

    return body_string.format(**kwargs)

def get_email_subject_person_added():
    return 'You have been added to a quality improvement project'

def __a_or_an(phrase):
    if phrase[0].lower() in 'aeiou':
        return 'an'
    return 'a'
