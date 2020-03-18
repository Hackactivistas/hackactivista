from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
# from pagedown.widgets import AdminPagedownWidget
# from martor.widgets import AdminMartorWidget
# from .models import *


# class Seo_resource(resources.ModelResource):

#     class Meta:
#         model = SeoBlog
#         exclude = ()

# class Seo_admin(ImportExportModelAdmin):
#     resource_class = Seo_resource
#     search_fields = (
#     	'keyword',
#     	'title', 'description', 
#     	'published_time', 'modified_time' 
#     	)
#     list_display = ('keyword',
#     				'title', 'description', 
#     				'published_time', 
#     				'modified_time' )

# admin.site.register(SeoBlog, Seo_admin)