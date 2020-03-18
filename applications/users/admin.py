from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

# from .models import Usuario, Perfil_usuario, Testimonio, Terminos, Politicas
from .models import *
from .forms import CustomUserChangeForm, CustomUserCreationForm

from import_export import resources
from import_export.admin import ImportExportModelAdmin
# from pagedown.widgets import AdminPagedownWidget
from easy_select2 import select2_modelform
from django.forms import Textarea

# Register your models here.
from django.contrib.auth.models import Group
# desregistramos GROUP para poder agregar IMMPORTAR E Exportar todos lo
# grupos GENERADOS
admin.site.unregister(Group)


class UsuarioResource(resources.ModelResource):

    class Meta:
        model = Usuario
        # fields = ('id',
        #           'usuario',
        #           'dni',
        #           'apellidos',
        #           'nombres',
        #           'sexo',
        #           'celular',
        #           'email',
        #           'is_superuser',
        #           'is_staff',
        #           'is_active',
        #           'groups',
        #           'date_joined'
        #           )
        # exclude = ('password',
        #           'last_login',
        #           'user_permissions')
        exclude = ()


class UsuarioAdmin(ImportExportModelAdmin):
    resource_class = UsuarioResource


# Aqui integramos UserAdmin de todos los LISTAS de usuarios y
# UsuarioAdmin para importar y exportar

# En este caso agregaremos en Usuario su Perfil

class ProfileInline(admin.StackedInline):
    model = Perfil_usuario
    can_delete = False
    verbose_name_plural = 'Perfil usuario'
    fk_name = 'usuario'
    # para agrgar solo un perfil, por defecto lo agregara varios
    # eso es lo que no queremos
    extra = 1
    # max 1, porque la relacion es 1 a 1
    max_num = 1
    min_num = 1


class CustomUserAdmin(UserAdmin, UsuarioAdmin):

    # para agregar perfil de usuario a Usuario
    inlines = (ProfileInline, )
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('usuario', 'password')}),
        (_('Personal info'), {
         'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('usuario', 'email', 'password1', 'password2')}
         ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('usuario', 'get_nombres', 'get_apellidos', 'get_celular',
                    'get_pais', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_active', 'groups__name')
    list_editable = ('is_active',)
    search_fields = ('usuario', 'email')
    ordering = ('-date_joined',)

    # relacionar con un nombre para poder acceder a sus atributos de perfil Usuario
    # esto funcionara solo con relaciones OneToOneField
    list_select_related = ('perfil_usuario', )

    # para agregar Perfil de Usuario
    # para mostrar campos de perfil de Usuario en Usario(list_display)

    def get_nombres(self, instance):
        return instance.perfil_usuario.nombres
    get_nombres.short_description = 'Nombres'

    def get_apellidos(self, instance):
        return instance.perfil_usuario.apellidos
    get_apellidos.short_description = 'Apellidos'

    def get_celular(self, instance):
        return instance.perfil_usuario.celular
    get_celular.short_description = 'Celular'

    def get_pais(self, instance):
        return instance.perfil_usuario.pais
    get_pais.short_description = 'Pais'

    # Mostrar con su perfil el usuario
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# registrando los modelos en el admin

# para asignar importar e Exportar en GRUPOS
# para eventos
class Group_resource(resources.ModelResource):

    class Meta:
        model = Group
        exclude = ()


class Group_admin(ImportExportModelAdmin):
    resource_class = Group_resource
    filter_horizontal = ('permissions', )


class Perfil_usuario_resource(resources.ModelResource):

    class Meta:
        model = Perfil_usuario
        exclude = ()


class Perfil_usuario_admin(ImportExportModelAdmin):
    list_display = ('usuario', 'nombres',
                    'apellidos', 'celular', 'pais',
                    'ocupacion')
    search_fields = ('nombres', 'apellidos',
                     'celular', 'pais')
    list_filter = ('pais','empresa')
    resource_class = Perfil_usuario_resource


admin.site.register(Group, Group_admin)
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Perfil_usuario, Perfil_usuario_admin)
