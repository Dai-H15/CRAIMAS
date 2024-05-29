from django.contrib import admin
from .models import Companies, About, Idea, Motivation, D_Company, Adoption, RegistSets, Interview, Interviewer
# Register your models here.


class RegistSetsAdmin(admin.ModelAdmin):
    model = RegistSets
    list_display = ("get_company_name", "by_U_ID", "created")
    search_fields = ["company__name", "by_U_ID"]

    def get_company_name(self, obj):
        return obj.company.name
    get_company_name.short_description = 'Company Name'


admin.site.register(RegistSets, RegistSetsAdmin)
admin.site.register(Companies)
admin.site.register(About)
admin.site.register(Idea)
admin.site.register(Motivation)
admin.site.register(D_Company)
admin.site.register(Adoption)
admin.site.register(Interview)
admin.site.register(Interviewer)