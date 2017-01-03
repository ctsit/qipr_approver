from django import template

register = template.Library()

@register.inclusion_tag('templatetags/form_select.html')
def form_select(input_dict, is_disabled=False):
    """
    Renders a drop down input selection.

    Keyword arguments:
    input_dict: a dictionary containing the fields to pass the HTML
    is_disabled: a boolean to determine if this field is disabled
    """
    input_dict['input_class_list'] = input_dict.get('input_classes') or []
    input_dict['div_class_list'] = input_dict.get('div_classes') or []

    if is_disabled:
        input_dict['is_disabled'] = "disabled"
    else:
        input_dict['is_disabled'] = ""
    return input_dict
