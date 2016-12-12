from django import template

from approver.models import Project

register = template.Library()

@register.inclusion_tag('templatetags/approved_certificate.html')
def approved_certificate(project):
    project_details = {
        'project_owner_first_name': project.owner.first_name,
        'project_owner_last_name': project.owner.last_name,
        'project_title': project.title,
        'project_collab': project.collaborator.all(),
        'project_approval_date': project.approval_date,
    }
    return project_details
