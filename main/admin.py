from django.contrib import admin
from .models import Companies, About, Idea, Motivation, D_Company, Adoption, RegistSets, Interview, Interviewer
# Register your models here.


class RegistSetsAdmin(admin.ModelAdmin):
    model = RegistSets
    list_display = ("company", "by_U_ID", "created")
    search_fields = ["company", "by_U_ID"]


admin.site.register(Companies)
admin.site.register(About)
admin.site.register(Idea)
admin.site.register(Motivation)
admin.site.register(D_Company)
admin.site.register(Adoption)
admin.site.register(RegistSets, RegistSetsAdmin)
admin.site.register(Interview)
admin.site.register(Interviewer)