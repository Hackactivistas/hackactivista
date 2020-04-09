"""hackactivista URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from applications.users.views import (change_password, 
                                        registro_usuario_modals, 
                                        Completar_registro_perfil,
                                        Registrarse, Index_principal,
                                        LogOut, userlogin,
                                        activate)
# para cambio de contraseña con redes scciales
from applications.users import views as core_views

urlpatterns = [
    # admin
    url(r'^administrador/', admin.site.urls),
    url(r'^$', Index_principal.as_view(), name="index_principal"),
    url(r'quienes-somos', TemplateView.as_view(
        template_name='quienes-somos.html'), name='p_quienes_somos'),
    url(r'proyectos/$', TemplateView.as_view(
        template_name='proyectos.html'), name='p_nuestros_proyectos'),
    path(r'covid19/', include(('applications.covid19.urls', 'app_cuvid19'), 
                    namespace='app_cuvid19')),
    url(r'coronavirus/evolucion-casos-covid-19-peru/$', TemplateView.as_view(
        template_name='casos-covid-19.html'), name='p-casos-covid-19'),

    url(r'team-hackactivistas', TemplateView.as_view(
        template_name='team-hackactivistas.html'), name='p_team_hackactivistas'),

    url(r'pagina-interes', TemplateView.as_view(
        template_name='pagina-interes.html'), name='p_pagina-interes'),

    url(r'proyectos/alerta-minsa', TemplateView.as_view(
        template_name='alerta-minsa.html'), name='p_alerta-minsa'),
    
    url(r'proyectos/bio-covid19', TemplateView.as_view(
        template_name='bio-covid19.html'), name='p_bio-covid19'),

    url(r'proyectos/chat-covid19', TemplateView.as_view(
        template_name='chat-covid19.html'), name='p_chat-covid19'),
        url(r'proyectos/kitchay-coronavida', TemplateView.as_view(
        template_name='kitchay-coronavida.html'), name='p_kitchay-coronavida'),
    

    # politicas y privacidad para pedir correo al memento de auntenticacion con redes socia.
    # url(r'^politicas$', Politicas.as_view(), name="p_politicas"),
    # url(r'^terminos$', Terminos.as_view(), name="p_terminos"),
    # para auntenticacion con redes sociales
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    # para forzar cambio de contraseña despues de haberse autenticado con
    # redes sociales
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^iniciar/$', userlogin, name="iniciar_sesion"),
    url(r'^salir/$', LogOut, name='cerrar_sesion'),
    # para recuperacion de contraseña
    url('^', include('django.contrib.auth.urls')),
    path(r'users/', include(('applications.users.urls', 'app_users'), namespace='app_users')),
    # para activar el correo
    path(r'registrarse/', Registrarse.as_view(), 
        name="registrarse_usuario"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    url(r'^completar_registro_usuario/$', Completar_registro_perfil.as_view(),
        name='completar_registro_perfil_usuario'),

    # editor django-markdown-editor
    url('martor/', include('martor.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.views import serve as static_serve
    staticpatterns = static(settings.STATIC_URL, view=static_serve)
    mediapatterns = static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = staticpatterns + mediapatterns + urlpatterns
