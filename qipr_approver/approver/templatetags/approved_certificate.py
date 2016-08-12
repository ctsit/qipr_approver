from django import template

register = template.Library()

@register.inclusion_tag('templatetags/approved_certificate.html')
def approved_certificate():
    return {}
