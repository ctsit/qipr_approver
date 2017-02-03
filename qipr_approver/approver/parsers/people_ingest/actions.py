from django.contrib.auth.models import User

from approver.models import Contact
from approver.utils import get_or_instantiate

fixture_user = User.objects.get(id=1)

def build_field_index_map(acc, header_line):
    model_mapping = {
        'display_name': 'display_name',
        'first_name': 'first_name',
        'gatorlink': 'gatorlink',
        'last_name': 'last_name',
        'middle_name': 'middle_name',
        'name_prefix': 'name_prefix',
        'name_suffix': 'name_suffix',
        'uf_business_email': 'business_email',
        'uf_business_fax': 'business_fax',
        'uf_business_phone': 'business_phone',
        'workingtitle': 'working_title',
    }
    csv_fields = [field.lower().strip() for field in header_line.split('|')]
    field_index_map = {}
    for field in csv_fields:
        if model_mapping.get(field):
            field_index_map[str(csv_fields.index(field))] = model_mapping.get(field)
    return field_index_map

def make_contact(field_index_map, line):
    csv_data = line.split('|')
    contact_dict = {}
    for index, datum in enumerate(csv_data):
        if str(index) in field_index_map:
            field_name = field_index_map[str(index)]
            contact_dict[field_name] = datum

    # If we got data with no email
    if (contact_dict.get('business_email').lower() == 'null'):
        return field_index_map

    contact = Contact(**contact_dict)

    fixture_save(contact)
    return field_index_map

def fixture_save(model):
    model.save(fixture_user)

actions = {
    'header': build_field_index_map,
    'data': make_contact,
}
