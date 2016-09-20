from django.db import models

from approver.models import Project, Provenance


class MeshModel(Provenance):
    date_added = models.DateField(null=True)
    major_revision_date = models.DateField(null=True)
    ui = models.CharField(max_length=10)

    class Meta:
        abstract = True

class DescQualModel(MeshModel):
    annotation = models.TextField(null=True)
    history_note = models.TextField(null=True)
    mesh_scope_note = models.TextField(null=True)

    class Meta:
        abstract = True

class PharmacologicalAction(Provenance):
    name = models.CharField(max_length=250)

class SemanticType(Provenance):
    value = models.CharField(max_length=10)
    description = models.CharField(null=True, max_length=50)

class Synonym(Provenance):
    name = models.CharField(null=True, max_length=50)
    pipe_separated = models.CharField(null=True, max_length=400)

class Entry(Provenance):
    name = models.CharField(null=True, max_length=50)
    pipe_separated = models.CharField(null=True, max_length=300)

class RegistryNumber(Provenance):
    name = models.CharField(max_length=200)

class Source(Provenance):
    name = models.CharField(max_length=200)

class Qualifier(MeshModel):
    qualifier_established = models.CharField(null=True, max_length=25)
    abbreviation = models.CharField(max_length=2)
    sub_heading = models.CharField(max_length=50)

class Descriptor(MeshModel):
    allowable_qualifiers = models.ManyToManyField(Qualifier, related_name='+')
    descriptor_class = models.CharField(null=True, max_length=1)
    descriptor_entry_version = models.CharField(null=True, max_length=100)
    descriptor_sort_version = models.CharField(null=True, max_length=300)
    major_descriptor_date = models.DateField(null=True)
    entry = models.ManyToManyField(Entry, related_name='descriptor')
    forward_reference = models.ManyToManyField('self')
    mesh_heading = models.CharField(max_length=150)
    mesh_tree_number = models.CharField(max_length=80)
    pharmacological_action = models.ManyToManyField(PharmacologicalAction)
    cas_registry_number = models.CharField(null=True, max_length=40)
    related_registry_number = models.ManyToManyField(RegistryNumber)
    semantic_type = models.ManyToManyField(SemanticType)

class SCR(MeshModel):
    frequency = models.IntegerField(null=True)
    heading_mapped_to = models.ManyToManyField(Descriptor, related_name='scr')
    indexing_information = models.ManyToManyField(Descriptor, related_name='scr_indexing')
    substance_name = models.CharField(null=True, max_length=300)
    substance_name_term_thesaurus = models.CharField(null=True, max_length=40)
    note = models.TextField()
    pharmacological_action = models.ManyToManyField(PharmacologicalAction)
    cas_registry_number = models.CharField(null=True, max_length=40)
    related_registry_number = models.ManyToManyField(RegistryNumber)
    source = models.ManyToManyField(Source)
    semantic_type = models.ManyToManyField(SemanticType)
    synonym = models.ManyToManyField(Synonym)

