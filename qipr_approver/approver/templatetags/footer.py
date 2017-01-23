from django import template
from approver.models import Project, Person, User
from django.utils import timezone

import approver.constants as constants

register = template.Library()

@register.inclusion_tag('templatetags/footer.html')
def footer():
    """
    Renders a footer with the version number found in constants
    """
    input_dict={
        'version_number': constants.VERSION_NUMBER,
        'count_registered_projects': 0,
        'count_monthly_projects': 0,
        'count_active_users': 0,
        'count_approved_projects': 0,
    }
    input_dict['count_registered_projects'] = Project.objects.count()
    input_dict['count_monthly_projects'] = Project.objects.filter(created__month=timezone.now().month).count()
    input_dict['count_active_users'] = User.objects.exclude(last_login=None).count()
    input_dict['count_approved_projects'] = Project.objects.exclude(approval_date=None).count()
    return input_dict
