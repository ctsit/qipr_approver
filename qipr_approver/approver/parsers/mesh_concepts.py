from django.contrib.auth.models import User

from approver.models import *
from approver.decorators import make_safe
from approver.utils import get_or_instantiate, save_all

fixture_user = User.objects.get(username='admin_fixture_user')

@make_safe
def parse_concepts(concept_list):
    concepts = concept_list.findall('Concept')

    return [get_or_create_concept(concept) for concept in concepts]

@make_safe
def get_or_create_concept(cnode):
    ui = cnode.find('ConceptUI').text

    model = get_or_instantiate(Concept, **{'concept_ui': ui})

    model.casn1_name = cnode.find('CASN1Name').text
    model.concept_ui = ui
    model.is_preferred_concept = True if cnode.get('PreferredConceptYN') == 'Y' or False
    model.name = cnode.find('ConceptName').find('String').text
    model.registry_number = cnode.find('RegistryNumber').text
    model.related_registry_number = get_registry_numbers(cnode.find('RelatedRegistryNumberList'))
    model.scope_note = cnode.find('ScopeNote').text
    model.term = get_terms(cnode.find('TermList'))

    #might need to clear these before hand
    model.narrower_concept = get_related_concepts(cnode.find('ConceptRelationList'), 'NRW')
    model.broader_concept = get_related_concepts(cnode.find('ConceptRelationList'), 'BRD')
    model.related_concept = get_related_concepts(cnode.find('ConceptRelationList'), 'REL')


def get_registry_numbers(rel_reg_list):
    models = [get_or_instantiate(RegistryNumber, **{'value':node.text}) for node in rel_reg_list.getchildren()]
    save_all(models, fixture_user)
    return models

def get_related_concepts(relation_list_node, relation):
    for relation_node in relation_list_node.getchildren():
        if relation in relation_node.get('RelationName'):
            desired_relation_list_node = relation_node
    models = []
    for node in desired_relation_list_node.getchildren():
        params = {'concept_ui': node.text}
        models.append(get_or_instantiate(Concept, **params))
    save_all(models, fixture_user)
    return models
