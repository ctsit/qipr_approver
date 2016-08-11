from django import template

register = template.Library()
 

@register.inclusion_tag('templatetags/address.html')
def address(address_model, address_type, counter=''):
    """
    Renders the address widget
    Takes the following parameters:

    * address_model: the address object passed from the user
    * address_type: the type of address used to id the div
    * optional counter: adds a counter to the html names to help make them unique
    """
    input_dict = {
        'address_type': address_type or '',
        'address_id': address_model.id or '',
        'counter': counter,
        'address1': address_model.address1 or '',
        'address2': address_model.address2 or '',
        'city': address_model.city or '',
        'zip_code': address_model.zip_code or '',
        'state': address_model.state or '',
        'country': address_model.country or '',
    }
    return input_dict
