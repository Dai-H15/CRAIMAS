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


class InterviewAdmin(admin.ModelAdmin):
    model = Interview
    list_display = ("title", "company_name", "InterviewID", "by_U_ID")
    search_fields = ["title", "company_name", "InterviewID", "by_U_ID"]


class InterviewerAdmin(admin.ModelAdmin):
    model = Interviewer
    list_display = ("name", "company_name__name", "by_U_ID",)
    search_fields = ["name", "company_name__name", "by_U_ID"]


admin.site.register(RegistSets, RegistSetsAdmin)
admin.site.register(Companies)
admin.site.register(About)
admin.site.register(Idea)
admin.site.register(Motivation)
admin.site.register(D_Company)
admin.site.register(Adoption)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(Interviewer, InterviewerAdmin)
