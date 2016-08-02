from django import template

register = template.Library()
 

@register.inclusion_tag('templatetags/address.html')
def address(address_model, address_type):
    """
    Renders the address widget
    Takes the following keywords:

    address_model: the address object passed from the user
    address_type: the type of address used to id the div
    """
    input_dict = {
        'address_type': address_type,
        'address1': address_model.address1,
        'address2': address_model.address2,
        'city': address_model.city,
        'zip_code': address_model.zip_code,
        'state': address_model.state,
        'country': address_model.country
    }
    return input_dict
