"""
This file contains constants for various things in the app.
DONT STRING MATCH
put stuff in here and import to other files.
Also dont import things into here, circular dependencies == bad
"""
gatorlink_header = 'Glid'
STATE_CHOICES = [
    ("FL", "Florida"),
]

COUNTRY_CHOICES = [
    ("US", "United States of America! YEAH!"),
]

SESSION_VARS = {
    'gatorlink': 'gatorlink',
    'email': 'email',
    'first_name': 'first_name',
    'last_name': 'last_name',
}

ADDRESS_TYPE= {
    'business': 'business',
    'organization': 'organization',
}

answer_submit_names = {
    'question_id': 'question_id',
    'choice_id': 'choice_id',
    'project_id': 'project_id',
}

answer_response_names = {
    'user_id': 'user_id',
    'question_id': 'question_id',
    'choice_id': 'choice_id',
    'project_id': 'project_id',
    'response_id': 'response_id',
    'newly_created': 'newly_created',
}
