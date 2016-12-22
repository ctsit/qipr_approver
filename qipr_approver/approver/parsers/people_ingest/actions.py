from django.contrib.auth.models import User

from approver.models import Person
from approver.utils import get_or_instantiate

fixture_user = User.objects.get(id=1)

def build_field_index_map(acc, header_line):
    model_mapping = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'gatorlink': 'gatorlink',
        'uf_business_email': 'email_address'
    }
    csv_fields = [field.lower() for field in header_line.split('|')]
    field_index_map = {}
    for field in csv_fields:
        if model_mapping.get(field):
            field_index_map[str(csv_fields.index(field))] = model_mapping.get(field)
    return field_index_map

def make_person(field_index_map, line):
    csv_data = line.split('|')
    person_dict = {}
    for index, datum in enumerate(csv_data):
        if str(index) in field_index_map:
            field_name = field_index_map[str(index)]
            person_dict[field_name] = datum

    if person_dict['gatorlink'] == 'NULL':
        return field_index_map

    person = get_or_instantiate(Person, {'gatorlink':person_dict['gatorlink']})
    for key in person_dict.keys():
        if not getattr(person, key):
            person = set_return(person, key, person_dict[key])

    fixture_save(person)
    return field_index_map

def fixture_save(model):
    model.save(fixture_user)

def set_return(model, prop, value, mapping=lambda x:x):
    setattr(model, prop, mapping(value))
    return model

actions = {
    'header': build_field_index_map,
    'data': make_person,
}
