from django.contrib.auth.models import User

from approver.models import *
import approver.utils as utils

fixture_user = Users.objects.get(id=1)

actions = {
    '*NEWRECORD': lambda acc, RHS: acc,
    'AN': lambda acc, RHS: set_return(acc, 'annotation', RHS),
    'AQ': lambda acc, RHS: set_qualifiers(acc, RHS),
    'CATSH': lambda acc, RHS: acc,
    # 'CX': lambda acc, RHS: set_consider_also(acc, RHS),
    'DA': lambda acc, RHS: set_date(acc, 'date_added', RHS),
    'DC': lambda acc, RHS: set_return(acc, 'descriptor_class', RHS),
    'DE': lambda acc, RHS: set_return(acc, 'descriptor_entry_version', RHS),
    'DQ': lambda acc, RHS: set_date(acc, 'qualifier_established', RHS),
    'DS': lambda acc, RHS: set_return(acc, 'descriptor_sort_version', RHS),
    'DX': lambda acc, RHS: set_date(acc, 'major_descriptor', RHS),
    # 'EC': lambda acc, RHS: set_return(acc, 'annotation', RHS),
    'FR': lambda acc, RHS: set_return(acc, 'frequency', RHS),
    # 'FX': lambda acc, RHS: set_return(acc, 'annotation', RHS),
    'HM': lambda acc, RHS: set_return(acc, 'heading_mapped_to', RHS),
    'HN': lambda acc, RHS: set_return(acc, 'history_note', RHS),
    'II': lambda acc, RHS: set_return(acc, 'indexing_information', RHS),
    'MH': lambda acc, RHS: set_return(acc, 'mesh_heading', RHS),
    'MH_TH': lambda acc, RHS: set_return(acc, 'mesh_heading_thesaurus', RHS),
    'MN': lambda acc, RHS: set_return(acc, 'mesh_tree_number', RHS),
    'MR': lambda acc, RHS: set_date(acc, 'major_revision_date', RHS),
    'MS': lambda acc, RHS: set_return(acc, 'mesh_scope_note', RHS),
    'N1': lambda acc, RHS: set_return(acc, 'castype1_name', RHS),
    'NM': lambda acc, RHS: set_return(acc, 'substance_name', RHS),
    'NM_TH': lambda acc, RHS: set_return(acc, 'substance_name_term_thesaurus', RHS),
    'NO': lambda acc, RHS: set_return(acc, 'note', RHS),
    'OL': lambda acc, RHS: set_return(acc, 'online_note', RHS),
    #some of these like PA have multiples for each mesh object. make something other than setreturn
    'PA': lambda acc, RHS: set_return(acc, 'pharmacological_action', RHS),
    'PI': lambda acc, RHS: set_return(acc, 'previous_indexing', RHS),
    'PM': lambda acc, RHS: set_return(acc, 'public_mesh_note', RHS),
    # this needs to be parsed out. complex data right now. Dont understand it
    # 'PRINT ENTRY': lambda acc, RHS: set_return(acc, 'print_entry', RHS),
    'QA': lambda acc, RHS: set_return(acc, 'topical_qualifier_abbreviation', RHS),
    'QE': lambda acc, RHS: set_return(acc, 'qualifier_entry_version', RHS),
    'QS': lambda acc, RHS: set_return(acc, 'qualifier_sort_version', RHS),
    'QT': lambda acc, RHS: set_return(acc, 'qualifier_type', RHS),
    # cross references need more help
    # 'QX': lambda acc, RHS: set_return(acc, 'qualifier_cross_reference', RHS),
    'RECTYPE': instantiate_mesh_model,
    'RH': lambda acc, RHS: set_return(acc, 'running_head', RHS),
    'RN': lambda acc, RHS: set_return(acc, 'RN_field', RHS),
    # multiples
    'RR': lambda acc, RHS: set_return(acc, 'related_registry_number', RHS),
    'SH': lambda acc, RHS: set_return(acc, 'sub_heading', RHS),
    'SO': lambda acc, RHS: set_return(acc, 'source', RHS),
    'ST': lambda acc, RHS: set_return(acc, 'semantic_type', RHS),
    'SY': lambda acc, RHS: set_return(acc, 'synonym', RHS),
    'TH': lambda acc, RHS: set_return(acc, 'thesaurus_identifier', RHS),
    'TN': lambda acc, RHS: set_return(acc, 'tree_node_allowed', RHS),
    'UI': lambda acc, RHS: set_return(acc, 'ui', RHS),
}

def instantiate_mesh_model(acc, RHS):
    model_funcs = {
        'D': Descriptor,
        'Q': Qualifier,
        'C': SCR,
    }
    return model_funcs[RHS]()

def set_add_return(obj, prop, value):
    #look up tables of the values that can happen in here
    manager = getattr(obj, prop)
    manager.add(value)
    return obj

def set_return(obj, prop, value):
    setattr(obj, prop, value)
    return obj

def parse_date(yyyymmdd):
    return None

def set_date(obj, prop, value):
    date = parse_date(value)
    return set_return(obj, prop, date)

def set_qualifiers(model, quals):
    quals = quals.split(' ')
    for qual in quals:
        if len(qual) == 2:
            qualifier = utils.get_or_instantiate(Qualifier, **{'abbreviation': qual})
            qualifier.save(fixture_user)
            model.allowable_qualifiers.add(qualifier)
    return model

def set_consider_also(model, RHS):
    # there arent very many of these but we will want to break them into something
    # nicer than just the nasty string that they are now
    model.consider_also = RHS
    return model
