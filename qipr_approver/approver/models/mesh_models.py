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

    def __str__(self):
        return str(self.name)

class SemanticType(Provenance):
    value = models.CharField(max_length=10)
    description = models.CharField(null=True, max_length=50)

    def __str__(self):
        return str(self.value)

class Synonym(Provenance):
    name = models.CharField(null=True, max_length=50)
    pipe_separated = models.CharField(null=True, max_length=400)

    def __str__(self):
        return str(self.name)

class Entry(Provenance):
    name = models.CharField(null=True, max_length=50)
    pipe_separated = models.CharField(null=True, max_length=300)

    def __str__(self):
        return str(self.name)

class RegistryNumber(Provenance):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

class Source(Provenance):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

class MeshTreeNumber(Provenance):
    value = models.CharField(max_length=100)

    def __str__(self):
        return str(self.value)

    def get_value_at_index(self, index):
        return self.number.split('.')[index] or None


class Qualifier(MeshModel):
    qualifier_established = models.CharField(null=True, max_length=25)
    abbreviation = models.CharField(max_length=2)
    sub_heading = models.CharField(max_length=50)

    def __str__(self):
        return str(self.sub_heading)

class Descriptor(MeshModel):
    allowable_qualifiers = models.ManyToManyField(Qualifier, related_name='+')
    cas_registry_number = models.CharField(null=True, max_length=40)
    descriptor_class = models.CharField(null=True, max_length=1)
    descriptor_entry_version = models.CharField(null=True, max_length=100)
    descriptor_sort_version = models.CharField(null=True, max_length=300)
    entry = models.ManyToManyField(Entry, related_name='descriptor')
    forward_reference = models.ManyToManyField('self')
    major_descriptor_date = models.DateField(null=True)
    mesh_heading = models.CharField(max_length=150)
    mesh_tree_number = models.ForeignKey(MeshTreeNumber, on_delete=models.CASCADE, related_name='descriptor', null=True)
    pharmacological_action = models.ManyToManyField(PharmacologicalAction)
    related_registry_number = models.ManyToManyField(RegistryNumber)
    semantic_type = models.ManyToManyField(SemanticType)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='mesh_keyword', null=True)
    tag_property_name = 'mesh_heading'

    def __str__(self):
        return str(self.mesh_heading)

class SCR(MeshModel):
    cas_registry_number = models.CharField(null=True, max_length=40)
    frequency = models.IntegerField(null=True)
    heading_mapped_to = models.ManyToManyField(Descriptor, related_name='scr')
    indexing_information = models.ManyToManyField(Descriptor, related_name='scr_indexing')
    note = models.TextField()
    pharmacological_action = models.ManyToManyField(PharmacologicalAction)
    related_registry_number = models.ManyToManyField(RegistryNumber)
    semantic_type = models.ManyToManyField(SemanticType)
    source = models.ManyToManyField(Source)
    substance_name = models.CharField(null=True, max_length=300)
    substance_name_term_thesaurus = models.CharField(null=True, max_length=40)
    synonym = models.ManyToManyField(Synonym)

    def __str__(self):
        return str(self.substance_name)
