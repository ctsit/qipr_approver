from django import template

register = template.Library()

@register.inclusion_tag('templatetags/form_input_textarea.html')
def form_input_textarea(input_dict, is_disabled=False):
    """
    Renders a textarea with a label.
    Takes the following keywords:

    name: the name that corresponds to the input, will be in form when submitted
    label: the string that will be displayed as a label
    value: the value of the input. Not checked or validated
    """
    input_classes = input_dict.get('input_classes') or []
    input_dict['input_class_list'] = ' '.join([str(cls) for cls in input_classes])
    input_dict['required'] = 'required_form-input' if input_dict.get('required') else ''
    if is_disabled:
        input_dict['is_disabled'] = "disabled"
    else:
        input_dict['is_disabled'] = ""
    return input_dict
