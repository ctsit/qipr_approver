import os
"""
This file contains constants for various things in the app.
DONT STRING MATCH
put stuff in here and import to other files.
Also dont import things into here, circular dependencies == bad
"""

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

answer_submit_names = {
    'question_id': 'question_id',
    'choice_id': 'choice_id',
    'project_id': 'project_id',
}

projects_per_page = 25

description_factor = 25

keyword_factor = 25

title_factor = 10

big_aim_factor = 10

category_factor = 10

clinical_area_factor = 10

clinical_setting_factor = 10

api_username = 'admin_api_user'

gatorlink_header = 'Glid'

registry_host = 'http://' + os.environ['QIPR_APPROVER_REGISTRY_HOST']

registry_endpoints = {
    'add_model': '/'.join([registry_host, 'add_model']),
}

app_label = 'approver'

VERSION_NUMBER = '0.5.0'

