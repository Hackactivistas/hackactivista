from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from requests.api import request

from .models import Usuario, Perfil_usuario
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import *
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
# import md5
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from hackactivista import settings
from hackactivista.settings.email_info import * 
# para validacion de contraseñas
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext as _
# para cambio de contraseñas
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# para autenticacion con redes sociales
from social_django.models import UserSocialAuth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
# settings y password para controlar autenticacion con redes sociales
# envio de correo cuando apertura una cuenta
from django.conf import settings 
# from django.core.mail import send_mail
from applications.emails.views import send_mail
# para autenticacion persozalizdo
from .functions import UsernameOrEmailBackend

# from django.core.urlresolvers import reverse
from django.urls import reverse_lazy, reverse
# para tokens, por ejemplo para confirmacion de email
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
import time

@login_required
def settings(request):
    user = request.user

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() >
                      1 or user.has_usable_password())

    return render(request, 'usuarios/settings.html', {
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, 'Su contraseña fue actualizada con éxito!')
            return redirect('password')
        else:
            messages.error(
                request, 'Por favor corrija el error a continuación.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'usuarios/password.html', {'form': form})


class Index_principal(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index_principal,
                        self).get_context_data(**kwargs)
        # context['inscripcion_usuario'] = UsuarioForm()

        # context['banners'] = Banner.objects.filter(
        #     estado=True).order_by('-fecha_publicacion')[:1]
        # context['eventos'] = Evento.objects.filter(
        #     estado=True).order_by('-fecha_creacion')[:1]
        
        # Mostramos un alert en caso que un usuario no ha completado sus datos
        estado_registro_completado = False 
        if self.request.user.is_authenticated:
            user = get_object_or_404(
                Usuario, usuario=self.request.user.usuario)
            if not user.perfil_usuario.nombres or not user.perfil_usuario.apellidos:
                estado_registro_completado = True
            else:
                estado_registro_completado = False

        context['estado_registro_completado'] = estado_registro_completado
        return context


def userlogin(request):
    next = request.GET.get('next', '/')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        # user = UsernameOrEmailBackend()
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("usuario inactivo, por favor confirme su cuenta o contáctenos al wsp : 965791848.")
        else:
            messages.error(
            request, 'Correo o contraseña no son correctos..!', extra_tags='danger')
            # return HttpResponseRedirect('/iniciar/')
            return render(request, "users/login.html", {'redirect_to': next})
    return render(request, "users/login.html", {'redirect_to': next})


def LogOut(request):
    logout(request)
    return HttpResponseRedirect('/')

class UsuarioEditar(LoginRequiredMixin, UpdateView):

    template_name = 'usuarios/editar_usuario.html'
    success_url = reverse_lazy('app_usuarios:p_inicio')
    model = Usuario
    form_class = UsuarioForm

    def form_valid(self, form):
        if self.request.POST['password'] != '':
            form.instance.set_password(self.request.POST['password'])
        else:
            pass
        # antes capturamos a que grupo pertenecia este usuario, para luego
        # actualizarlo
        pk_user = form.instance.pk
        usuario = get_object_or_404(Usuario, pk=pk_user)
        nombre_grupo = None
        for g_name in usuario.groups.all():
            nombre_grupo = g_name.name
        # forzamos el guardado de datos para poder asignar al grupo
        self.object = form.save()
        # y lo guardamos de nuevo al grupo que pertenecia antes, caso contrario
        # el grupo que ha estado agregado se liimpiaria
        p_grupo = get_object_or_404(Group, name=nombre_grupo)
        form.instance.groups.add(p_grupo)
        # agregamos al grupo establecido por el REGISTRADOR
        # redireccionamos al final, OJO: no estamos usando SUPER
        return HttpResponseRedirect(self.get_success_url())


class UsuarioEliminar(LoginRequiredMixin, DeleteView):

    template_name = 'usuarios/eliminar_usuario.html'
    model = Usuario
    success_url = reverse_lazy('app_usuarios:p_inicio')
    context_object_name = 'usuarios'

# Pueden registrar solo los admin


class Usuario_crear(LoginRequiredMixin, CreateView):
    form_class = UsuarioForm
    template_name = 'usuarios/crear_usuario.html'
    success_url = reverse_lazy('app_usuarios:p_inicio')
    user_register = UsuarioForm

    def form_valid(self, form):
        form.instance.set_password(self.request.POST['password'])
        # forzamos el guardado de datos para poder asignar al grupo
        self.object = form.save()
        grupo = get_object_or_404(Group, pk=self.request.POST['tipo_usuario'])
        # agregamos al grupo establecido por el REGISTRADOR
        form.instance.groups.add(grupo)
        # redireccionamos al final, OJO: no estamos usando SUPER
        # generamos su perfil de Usuario
        Perfil_usuario.objects.create(usuario=self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(
            Usuario_crear, self).get_context_data(*args, **kwargs)
        # mostramos todos los grupos a la pertenecera un USUARIO
        grupos = Group.objects.all()
        context_data['grupos'] = grupos
        return context_data


def registro_usuario_modals(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.instance.set_password(request.POST['password'])
            insert = form.save()
            # NOTA: cuidado si cambian de nombre al grupo habrá error
            grupo = Group.objects.get_or_create(name='Emprendedor')
            insert.groups.add(grupo)
            Perfil_usuario.objects.create(usuario=insert)
            # cuando termine de registrarse, automaticamente
            # iniciamos su sesion de Usuario
            user = authenticate(email=request.POST[
                                'email'], password=request.POST['password'])
            asunto = "Apertura de cuenta | Future Startup Hero"
            mensaje = ('Bienvenido, se ha registrado en Future Starup Hero.\n '
                    'Correo :' + user.email + '\n'
                    'usuario : ' + user.usuario + '\n'
                    'http://futurestartuphero.com')
            send_mail(asunto, mensaje, EMAIL_HOST_USER, [user.email])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    perfil = Perfil_usuario_form()
                    return render(request, 'completar_registro_usuario.html',
                                  {'datos_perfil': perfil, 'usuario': insert.pk})
                else:
                    return HttpResponse("usuario inactivo.")
            else:
                return HttpResponseRedirect('iniciar/')

        else:
            usuario_form = UsuarioForm(form)
            messages.error(
                request, 'Por favor corrija los datos..!', extra_tags='danger')
            return render(request, 'registrarse.html', {'form': usuario_form})
    else:
        return redirect('/')


class Completar_registro_perfil(LoginRequiredMixin, UpdateView):
    form_class = Perfil_usuario_form
    template_name = 'registro-extra.html'
    success_url = reverse_lazy('index_principal')

    # esto es importantisimo, nos permite editar sin pasar por URL
    def get_object(self):
        print ("HOLA-->", self.request.user.usuario)
        usuario = get_object_or_404(Usuario, usuario=self.request.user.usuario)
        print ('USER:', usuario)
        # Interes_curso.objects.get_or_create(usuario=usuario)
        return get_object_or_404(Perfil_usuario, usuario__usuario=usuario.usuario)

class Registrarse(SuccessMessageMixin, CreateView):
    form_class = UsuarioForm
    template_name = 'users/register-user.html'
    success_url = reverse_lazy('index_principal')
    # user_register = UsuarioForm
    # success_message  = ()

    def form_valid(self, form):
        form.instance.set_password(self.request.POST['password'])
        # forzamos el guardado de datos para poder asignar al grupo
        self.object = form.save()
        self.object.is_active = True
        self.object.save()
        Perfil_usuario.objects.create(usuario=self.object, 
            celular= self.request.POST.get('celular'))
        # envio de confirmacion al correo 
        # current_site = get_current_site(self.request)
        # mensaje = render_to_string('acc_active_email.html', {
        #     'user':self.object, 'domain':current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
        #     'token': account_activation_token.make_token(self.object),
        # })

        mensaje = 'Bienvenido a Hackactivistas'
        user = authenticate(email=self.request.POST['email'], 
                            password=self.request.POST['password'])
        if user is not None:
            user.is_active = True
            user.save()
            login(self.request, user)
                

        # asunto = "Confirma tu correo en Hackactivistas"
        # send_mail(
        #     asunto, 
        #     'Registro de usuario en Future Startup Hero',
        #     EMAIL_HOST_USER, 
        #     [self.object.email],
        #     html_message=mensaje,
        #     fail_silently=False)
        grupo, created = Group.objects.get_or_create(name='usuario')
        grupo.user_set.add(self.object)
        messages.success(self.request, '''Gracias por registrarse.!''')
        # return super(Registrarse, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())
# verificar si un usuario ya existe, registro de formularios

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user.usuario, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Su contraseña se ha actualizada con éxito!')
            return redirect('app_usuarios:change_password')
        else:
            messages.error(request, 'Corrija el error a continuación.')
    else:
        form = PasswordChangeForm(request.user.usuario)
    return render(request, 'usuarios/cambio_contrasena.html', {
        'form': form
    })


@login_required
def cambio_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Su contraseña se ha actualizada con éxito!')
            # es importante pasar el parametro porque la Url es con nombre usuario
            return render(request, 'usuarios/perfil/cuenta.html', 
                                    {'form_password': PasswordChangeForm(request.user)})
        else:
            messages.error(request, 'Corrija el error a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'usuarios/perfil/cuenta.html', {
        'form_password': form
    })


class Ver_perfil(LoginRequiredMixin, TemplateView):
    """docstring for Ver_perfil"""
    template_name = 'usuarios/perfil/ver_perfil.html'

    def get_context_data(self, **kwargs):
        context = super(Ver_perfil,self).get_context_data(**kwargs)
        proyectos = Proyecto.objects.filter(usuario = self.request.user)
        context['proyectos'] = proyectos
        context['estado'] = proyectos.exists()
        context['estado'] = proyectos.exists()
        context['cantidad_proyectos'] = proyectos.count()
        return context



class Editar_perfil(LoginRequiredMixin,SuccessMessageMixin, UpdateView):

    template_name = 'usuarios/perfil/editar_perfil.html'
    form_class = Perfil_usuario_editar_form
    success_url = reverse_lazy('app_usuarios:p_editar_perfil',  args=['request.user.usuario'])
    success_message = "Ha actualizado correctamente sus datos..!"

    def get_object(self):
        return Perfil_usuario.objects.get(usuario=self.request.user.pk)

class Cuenta_usuario(LoginRequiredMixin, TemplateView):
    """docstring for Ver_perfil"""
    template_name = 'usuarios/perfil/cuenta.html'

    def get_context_data(self, **kwargs):
        context = super(Cuenta_usuario,self).get_context_data(**kwargs)
        context['form'] = UsuarioForm()
        context['form_password'] = PasswordChangeForm(self.request.user)
        return context

class Cambiar_cuenta_usuario(LoginRequiredMixin,SuccessMessageMixin, UpdateView):

    template_name = 'usuarios/perfil/cuenta.html'
    form_class = UsuarioForm_usaurio
    success_url = reverse_lazy('app_usuarios:p_cuenta',  args=['request.user.usuario'])
    success_message = "Se ha actualizado correctamente sus datos de Cuenta..!"

    def get_object(self):
        return Usuario.objects.get(usuario=self.request.user.usuario)

    def get_context_data(self, **kwargs):
        context = super(Cambiar_cuenta_usuario,self).get_context_data(**kwargs)
        context['form_password'] = PasswordChangeForm(self.request.user)
        return context



    # para activar la cuen

# para activar la cuenta via confirmacion de CORREO
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return HttpResponseRedirect(reverse('completar_registro_perfil_usuario'))

    else:
        return HttpResponse('¡El enlace de activación no es válido!')

