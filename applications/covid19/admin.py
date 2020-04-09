from django.contrib import admin
from .models import DiagnosisCovid19
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class DiagnosisCovid19Resource(resources.ModelResource):

    class Meta:
        model = DiagnosisCovid19
        exclude = ()


class DiagnosisCovid19Admin(ImportExportModelAdmin):
	list_display = ('user_upload','date_register','img', 'status_process')
	list_editable = ('status_process',)
	resource_class = DiagnosisCovid19Resource

admin.site.register(DiagnosisCovid19, DiagnosisCovid19Admin)