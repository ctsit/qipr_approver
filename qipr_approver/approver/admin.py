from django.contrib import admin

from .models import *

class ProvenanceAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        user = request.user
        #obj.after_create(user)
        obj.save(last_modified_by=user)

admin.site.register(Person,ProvenanceAdmin)
admin.site.register(Project,ProvenanceAdmin)
admin.site.register(Position,ProvenanceAdmin)
admin.site.register(Speciality,ProvenanceAdmin)
admin.site.register(Organization,ProvenanceAdmin)
admin.site.register(Category,ProvenanceAdmin)
admin.site.register(BigAim,ProvenanceAdmin)
admin.site.register(FocusArea,ProvenanceAdmin)
admin.site.register(ClinicalDepartment,ProvenanceAdmin)
admin.site.register(Address,ProvenanceAdmin)
admin.site.register(Training,ProvenanceAdmin)
admin.site.register(Keyword,ProvenanceAdmin)
admin.site.register(SafetyTarget,ProvenanceAdmin)
admin.site.register(ClinicalArea,ProvenanceAdmin)
admin.site.register(ClinicalSetting,ProvenanceAdmin)
admin.site.register(Suffix,ProvenanceAdmin)
admin.site.register(Expertise,ProvenanceAdmin)
admin.site.register(QI_Interests,ProvenanceAdmin)
admin.site.register(Section,ProvenanceAdmin)
admin.site.register(Question,ProvenanceAdmin)
admin.site.register(Choice,ProvenanceAdmin)
admin.site.register(Response,ProvenanceAdmin)
