from django.contrib import admin
from .models import Candidate, Company

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_display_name', 'company_username')
    
admin.site.register(Candidate)
admin.site.register(Company,CompanyAdmin)