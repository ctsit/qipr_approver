import os
import configparser

config = configparser.ConfigParser()
config.read('/var/www/qipr_approver/qipr_approver/deploy/settings.ini')

def get_config(key):
    return config.get(config.default_section, key)

os.environ['DJANGO_SETTINGS_MODULE'] = "qipr_approver.settings"

os.environ['DJANGO_CONFIGURATION'] = get_config('configuration')
os.environ['DJANGO_SECRET_KEY'] = get_config('secret_key')
os.environ['DJANGO_WSGI'] = 'qipr_approver.wsgi.application'

os.environ['QIPR_APPROVER_DATABASE_NAME'] = get_config('database_name')
os.environ['QIPR_APPROVER_DATABASE_USER'] = get_config('database_user')
os.environ['QIPR_APPROVER_DATABASE_PASSWORD'] = get_config('database_password')
os.environ['QIPR_APPROVER_DATABASE_HOST'] = get_config('database_host')
os.environ['QIPR_APPROVER_DATABASE_PORT'] = get_config('database_port')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
