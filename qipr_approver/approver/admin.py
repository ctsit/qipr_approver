from django.contrib import admin

from .models import *

class ProvenanceAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        user = request.user
        obj.after_create(user)
        obj.save(last_modified_by=user)

admin.site.approver(Person,ProvenanceAdmin)
admin.site.approver(Project,ProvenanceAdmin)
admin.site.approver(Position,ProvenanceAdmin)
admin.site.approver(Speciality,ProvenanceAdmin)
admin.site.approver(Organization,ProvenanceAdmin)
admin.site.approver(Category,ProvenanceAdmin)
admin.site.approver(Address,ProvenanceAdmin)
admin.site.approver(Training,ProvenanceAdmin)
admin.site.approver(Keyword,ProvenanceAdmin)
admin.site.approver(SafetyTarget,ProvenanceAdmin)
admin.site.approver(ClinicalArea,ProvenanceAdmin)
admin.site.approver(ClinicalSetting,ProvenanceAdmin)
admin.site.approver(Suffix,ProvenanceAdmin)
admin.site.approver(Expertise,ProvenanceAdmin)
admin.site.approver(QI_Interests,ProvenanceAdmin)
admin.site.approver(Section,ProvenanceAdmin)
admin.site.approver(Question,ProvenanceAdmin)
admin.site.approver(Choice,ProvenanceAdmin)
admin.site.approver(Response,ProvenanceAdmin)
