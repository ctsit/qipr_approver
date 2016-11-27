from django import template
from approver.models import Project, Person
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
    input_dict['count_registered_projects'] = Project.objects.all().count()
    input_dict['count_monthly_projects'] = len([x for x in Project.objects.all() if x.created.month == timezone.now().month])
    input_dict['count_active_users'] = len([x for x in Person.objects.all() if (x.account_expiration_time == None) or (x.account_expiration_time > timezone.now())])
    input_dict['count_approved_projects'] = Project.objects.all().filter(approval_date__isnull=False).count()
    return input_dict
