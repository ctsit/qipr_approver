from django import template

register = template.Library()

@register.inclusion_tag('templatetags/question.html')
def question(input_dict):
    """
    """
    return input_dict
