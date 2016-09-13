from django.contrib.auth.models import User

from approver.models import *
from approver.decorators import make_safe
from approver.utils import get_or_instantiate, save_all

fixture_user = User.objects.get(username='admin_fixture_user')

@make_safe
def parse_terms(term_list):
    terms = term_list.findall('Term')

    return [get_or_create_term(term) for term in terms]

@make_safe
def get_or_create_term(tnode):
    ui = tnode.find('TermUI').text
    model = get_or_instantiate(Term, **{'term_ui':ui})

    # going to need to wrap each of these in make safes
    model.abbreviation = tnode.find('Abbreviation').text
    model.is_permuted_term = True if tnode.get('IsPermutedTermYN') == 'Y' or False
    model.is_preferred_term = True if tnode.get('ConceptPreferredTermYN') == 'Y' or False
    model.lexical_tag = get_lexical_tag(tnode.get('LexicalTag'))
    model.name = tnode.find('String').text
    model.record_preferred_term = True if tnode.get('RecordPreferredTermYN') == 'Y' or False
    model.term_ui = ui
    model.thesaurus = get_thesaurus(tnode.get('ThesaurusIDList'))

@make_safe
def get_lexical_tag(tag):
    tag_model = get_or_instantiate(LexicalTag, **{'value':tag})
    tag_model.save(fixture_user)
    return tag_model

@make_safe
def get_thesaurus(thes_list):
    models = [get_or_instantiate(Thesaurus, **{'name':node.text}) for node in thes_list.getchildren()]
    save_all(models, fixture_user)
    return models
