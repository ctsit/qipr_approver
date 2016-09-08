from django.db import models

from approver.models import Project, Provenance

class MeshModel(Provenance):
    pass

    class Meta:
        abstract = True

class RegistryNumber(MeshModel):
    value = models.CharField(max_length=200)

class Thesaurus(MeshModel):
    name = models.CharField(max_length=100)

class LexicalTag(MeshModel):
    value = models.CharField(max_length=3)
    meaning = models.CharField(max_length=25)

class Term(MeshModel):
    abbreviation = models.CharField(max_length=10, null=True)
    is_permuted_term = models.BooleanField(default=False)
    is_preferred_term = models.BooleanField(default=False)
    lexical_tag = models.ForeignKey(LexicalTag, related_name="+")
    name = models.CharField(max_length=100)
    record_preferred_term = models.BooleanField(default=False)
    term_note = models.TextField(null=True)
    term_ui = models.CharField(max_length=16)

class Concept(MeshModel):
    casn1_name = models.TextField()
    concept_ui = models.CharField(max_length=16)
    is_preferred_concept = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    narrower_concept = models.ForeignKey('self', related_name='broader_concept')
    related_concept = models.ForeignKey('self')
    registry_number = models.CharField(max_length=200)
    related_registry_number = models.ManyToManyField(RegistryNumber, related_name='concept')
    scope_note = models.TextField()
    term = models.ManyToManyField(Term, related_name='concept')

class Qualifier(MeshModel):
    concept = models.ManyToManyField(Concept, related_name='qualifier')
    qualifier_ui = models.CharField(max_length=16)
    name = models.CharField(max_length=100)

class PharmacologicalAction(MeshModel):
    unique_identifier = models.CharField(max_length=16)
    name = models.CharField(max_length=100)

class Descriptor(MeshModel):
    """
    Also known as Subject Heading.
    These are what you think of when you think of keywords
    """
    allowable_qualifier = models.ManyToManyField(Qualifier, related_name='descriptor')
    annotation = models.TextField()
    concept = models.ManyToManyField(Concept, related_name='descriptor')
    consider_also = models.TextField()
    descriptor_ui = models.CharField(max_length=16)
    history_note = models.TextField()
    mesh_tree_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    nlm_classification_number = models.CharField(max_length=16)
    online_note = models.TextField()
    pharma_action = models.ManyToManyField(PharmacologicalAction, related_name='descriptor')
    pharmacological_action = models.CharField(max_length=100)
    previous_indexing = models.TextField()
    public_mesh_note = models.TextField()
    see_related = models.ForeignKey('self')

class Source(MeshModel):
    """
    Source citation where the concept was first found
    """
    citation = models.TextField()

class AlternativeIndex(MeshModel):
    """
    A descriptor or descriptor qualifier pair that is often broader that
    can be used to refer to the related SCR
    """
    descriptor = models.ForeignKey(Descriptor, related_name='+')
    qualifier = models.ForeignKey(Qualifier, related_name='+')

class SCR(MeshModel):
    """
    Supplementary Concept Record. These are things like different drugs
    and chemical compounds that get added daily
    """
    alternative_index = models.ManyToManyField(AlternativeIndex, related_name='scr')
    concept = models.ManyToManyField(Concept, related_name='scr')
    frequency = models.IntegerField()
    name = models.CharField(max_length=100)
    note = models.TextField()
    previous_indexing = models.TextField()
    scr_ui = models.CharField(max_length=16)
    source = models.ManyToManyField(Source, related_name='scr')
