from django import template

register = template.Library()


@register.inclusion_tag('templatetags/tagbox.html')
def tagbox(input_dict, is_disabled=False):
    """
    Renders tagbox widget
    Takes the following keywords:

    name: the name that corresponds to the input, will be in form when submitted
    label: the string that will be displayed as a label
    options: the different options you can select from, list values
    selected: the options selected, list of values
    """
    if is_disabled:
        input_dict['disabled'] = "disabled"
    else:
        input_dict['disabled'] = ""

    input_dict['selected'] = __add_invisible_spaces(input_dict['selected'])
    input_dict['selected_values_string'] = __to_hidden_input_string(input_dict.get('selected'))
    return input_dict

def __get_option_dict(model):
    invisible_space = u"\u200B"
    return {
        'display': (str(item) + invisible_space),
        'guid': model.guid,
    }

def __add_invisible_spaces(collection):
    return [__get_option_dict(item) for item in collection]

def __to_hidden_input_string(collection):
    return ';'.join(str(item) for item in collection)
