from approver.models import *
from approver.utils import get_or_instantiate, save_all
from approver.decorators import make_safe
from approver.parses import parse_concepts

fixture_user = User.objects.get(username='admin_fixture_user')

def parse_desc_xml(tree):
    """
    This is destructive. Any identifieable mesh descriptor will be overwritten
    """
    model = Descriptor()
    root = tree.getroot()

    model.descriptor_ui = get_ui(root)
    model.name = get_name(root)
    model.history_note = get_note_text('HistoryNote', root)
    model.online_note = get_note_text('OnlineNote', root)
    model.public_mes_note = get_note_text('PublicMeSHNote', root)
    model.previous_indexing = get_prev_indexing(root)
    model.pharma_action = get_pharm_action(root)
    model.mesh_tree_number = get_mesh_tree_number(root)
    model.concept = parse_concepts(root)

    model.allowable_qualifier.clear()
    for qual in get_quals(root):
        model.allowable_qualifier.add(qual)

    annotation = models.TextField()
    concept = models.ManyToManyField(Concept, related_name='descriptor')
    consider_also = models.TextField()
    nlm_classification_number = models.CharField(max_length=16)
    see_related = models.ForeignKey('self')


    return model

@make_safe
def get_ui(root):
    ui_node = root.find('DescriptorUI')
    return ui_node.text

@make_safe
def get_string_node_text(parent):
    return parent.find('String').text

@make_safe
def get_note_text(tag, root):
    return root.find(tag).text

@make_safe
def get_name(root):
    desc_name_node = root.find('DescriptorName')
    return = get_string_node_text(desc_name_node)

@make_safe
def get_quals(root):
    qual_list = root.find('AllowableQualifierList')
    params = {
        'tag': 'QualifierReferredTo',
        'prefix': 'Qualifier',
        'Model': Qualifier,
        'ModelUI': 'qualifier_ui',
        'ModelName': 'name',
    }
    quals = qual_list.findall('AllowableQualifier')
    return [get_or_create(item, **params) for item in quals]

@make_safe
def get_or_create(node, **kwargs):
    ref_node = node.find(kwargs.get('tag'))
    prefix = kwargs.get('prefix')
    model_kwargs = {}
    model_kwargs[kwargs.get('ModelUI')] = ref_node.find(prefix + 'UI')
    model_kwargs[kwargs.get('ModelName')] = ref_node.find(prefix + 'UI')
    model = get_or_instantiate(kwargs.get('Model'), **model_kwargs)
    model.save(fixture_user)
    return model

@make_safe
def get_prev_indexing(root):
    prev_ind_list = root.find('PreviousIndexingList')
    text = ''
    for item in prev_ind_list.findall('PreviousIndexing')
        text = text + item.text
    return text

@make_safe
def get_pharm_action(root):
    pharm_list = root.find('PharmacologicalActionList')
    pharm_actions = pharm_list.findall('PharmacologicalAction')
    params = {
        'tag': 'DescriptorReferredTo',
        'prefix': 'Descriptor',
        'Model': PharmacologicalAction,
        'ModelUI': 'unique_identifier',
        'ModelName': 'name',
    }
    return [get_or_create(action, **params) for action in pharm_actions]

@make_safe
def get_mesh_tree_number(root):
    num_list = root.find('TreeNumberList')
    text = ''
    for child in num_list.getchildren():
        text = text + child.text
    return text
