from django import template

register = template.Library()

@register.inclusion_tag('templatetags/form_input.html')
def form_input(input_dict):
    """
    Renders an input with a label.
    Takes the following keywords:

    name: the name that corresponds to the input, will be in form when submitted
    label: the string that will be displayed as a label
    html_id: the id that can be used as an html_selector for the input
    type: the input type. See w3 schools input types for information
    value: the value of the input. Not checked or validated
    """
    return input_dict
