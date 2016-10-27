from django import template
import approver.constants as constants

register = template.Library()

@register.inclusion_tag('templatetags/footer.html')
def footer():
    """
    Renders a footer with the version number found in constants
    """
    input_dict={'version_number': constants.VERSION_NUMBER}
    return input_dict
