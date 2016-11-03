from django import template

register = template.Library()

@register.inclusion_tag('templatetags/form_select.html')
def form_select(input_dict, is_disabled=False):
    """
    Renders an input with a label.
    Takes the following keywords:

    name: the name that corresponds to the input, will be in form when submitted
    label: the string that will be displayed as a label
    type: the input type. See w3 schools input types for information
    value: the value of the input. Not checked or validated
    placeholder: example text to prompt customers to fill in text fields
    """
    input_dict['input_class_list'] = input_dict.get('input_classes') or []
    input_dict['div_class_list'] = input_dict.get('div_classes') or []

    #if the there is a value and the value is not listed is list, add other
    if ((input_dict['value']) and (input_dict['value'] not in input_dict.get('options'))):
        input_dict['other'] = input_dict['value']

    if is_disabled:
        input_dict['is_disabled'] = "disabled"
    else:
        input_dict['is_disabled'] = ""
    return input_dict
