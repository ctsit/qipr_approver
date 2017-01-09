from django.contrib.auth.models import User

from approver.models import Project, Person
from approver.utils import get_or_instantiate

field_sep = '|'
fixture_user = User.objects.get(id=1)
relateds = ['owner', 'collaborator', 'collaborator_email']

def build_field_index_map(acc, header_line):
    model_mapping = {
        'project title': 'title',
        'project description': 'description',
        'outcome measures': 'measures',
        'pi email': 'owner',
        'collaborators': 'collaborator',
        'collaborator email': 'collaborator_email'
    }
    csv_fields = [field.lower() for field in header_line.split(field_sep)]
    field_index_map = {}
    for field in csv_fields:
        if model_mapping.get(field):
            field_index_map[str(csv_fields.index(field))] = model_mapping.get(field)
    return field_index_map

def make_project(field_index_map, line):
    csv_data = line.split(field_sep)
    project_dict = {}
    for index, datum in enumerate(csv_data):
        if str(index) in field_index_map:
            field_name = field_index_map[str(index)]
            project_dict[field_name] = datum

    project = get_or_instantiate(Project, {'title':project_dict['title']})

    for key in project_dict.keys():
        if key in relateds:
            pass
        else:
            project = set_return(project, key, project_dict[key])

    fixture_save(project)
    related_person_add(project, project_dict)

    return field_index_map

def related_person_add(project, project_dict):
    owner, collaborators = get_people(project_dict)

    fixture_save(owner)
    for each in collaborators:
        fixture_save(each)

    project.owner = owner
    for each in collaborators:
        project.collaborator.add(each)

def get_people(project_dict):
    owner = None
    collaborators = []
    email_string = project_dict['collaborator_email']
    owner_email = project_dict['owner']
    if '@' in owner_email:
        owner = get_or_instantiate(Person, {'email_address': owner_email})
    emails = [email.strip() for email in email_string.split(',')]
    emails = [email.split(' ') for email in emails]
    emails = [item for sublist in emails for item in sublist]
    for email in emails:
        collaborators.append(get_or_instantiate(Person, {'email_address':email}))

    return owner, collaborators

def fixture_save(model):
    if model:
        model.save(fixture_user)

def set_return(model, prop, value, mapping=lambda x:x):
    setattr(model, prop, mapping(value))
    return model

actions = {
    'header': build_field_index_map,
    'data': make_project,
}
