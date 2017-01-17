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
    'previous_log_id': 'previous_log_id',
    'timeout_time': 1217
}

QI_CHECK = {
    'no': 0,
    'yes': 1,
    'no_program': 2,
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

users_per_page = 25

description_factor = 25

keyword_factor = 25

title_factor = 10

big_aim_factor = 10

category_factor = 10

clinical_area_factor = 10

clinical_setting_factor = 10

api_username = 'admin_api_user'

gatorlink_header = 'Glid'

bridge_key = os.environ['QIPR_SHARED_BRIDGE_KEY']

protocol = 'http://' if (os.environ['DJANGO_CONFIGURATION'] == 'development') else 'https://'

registry_host = protocol + os.environ['QIPR_APPROVER_REGISTRY_HOST']

registry_port = os.environ['QIPR_APPROVER_REGISTRY_PORT']

registry_path = os.environ['QIPR_APPROVER_REGISTRY_PATH']

registry_hostport = registry_host + (':' + registry_port if registry_port else '')

registry_hostportpath = registry_hostport + ( registry_path if registry_path else '')

registry_endpoints = {
    'add_model': '/'.join([registry_hostport, 'api', 'add_model']),
}

base_url = protocol + os.environ['QIPR_APPROVER_APPROVER_HOST'] + os.environ['QIPR_APPROVER_APPROVER_PATH']

app_label = 'approver'

total_qualifiers_2017 = 80

SHIB_ENABLED = os.getenv('SHIB_ENABLED', 'false')

VERSION_NUMBER = '0.8.0'
