from django import template

register = template.Library()

@register.inclusion_tag('templatetags/form_input.html')
def form_input(input_dict, is_disabled=False):
    """
    Renders an input with a label.
    Takes the following keywords:

    name: the name that corresponds to the input, will be in form when submitted
    label: the string that will be displayed as a label
    type: the input type. See w3 schools input types for information
    value: the value of the input. Not checked or validated
    placeholder: example text to prompt customers to fill in text fields
    """
    input_classes = input_dict.get('input_classes') or []
    input_dict['input_class_list'] = ' '.join([str(cls) for cls in input_classes])
    if is_disabled:
        input_dict['is_disabled'] = "disabled"
    else:
        input_dict['is_disabled'] = ""
    return input_dict
