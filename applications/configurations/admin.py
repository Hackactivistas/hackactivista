from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# from pagedown.widgets import AdminPagedownWidget
from martor.widgets import AdminMartorWidget
# Register your models here

class TermsConditionResource(resources.ModelResource):

    class Meta:
        model = TermsCondition
        exclude = ()

class TermsConditionAdmin(ImportExportModelAdmin):
    list_display = ('content', 'date_create')
    resource_class = TermsConditionResource
    formfield_overrides = {
            models.TextField: {'widget': AdminMartorWidget },
        }

class PrivacyPoliceResource(resources.ModelResource):

    class Meta:
        model = PrivacyPolice
        exclude = ()

class PrivacyPoliceAdmin(ImportExportModelAdmin):
    list_display = ('content', 'date_create')
    resource_class = PrivacyPoliceResource
    formfield_overrides = {
            models.TextField: {'widget': AdminMartorWidget },
        }

admin.site.register(TermsCondition,TermsConditionAdmin)
admin.site.register(PrivacyPolice,PrivacyPoliceAdmin)