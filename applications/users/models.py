from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from django.conf import settings
from django.core.mail import send_mail

from django.core.exceptions import ValidationError
class CustomUserManager(BaseUserManager):

    # aqui falta agregar correo en caso de registrar correo por redes sociales
    # de momento solo estara disponible con usuario
    def _create_user(self, usuario, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        user, created = self.get_or_create(email=email)
        if created: 
            user.set_password(password)
            user.usuario=usuario
            user.last_login=now
            user.date_joined=now
            user.is_staff=is_staff
            user.is_active = True
            user.is_superuser = is_superuser
            user.save()
            grupo, created = Group.objects.get_or_create(name='Emprendedor')
            # get_or_create() didn't have to create an object.
            user.groups.add(grupo)
            Perfil_usuario.objects.create(usuario=user)
        else:
            # user.set_password(password)
            # user.usuario = usuario
            # user.is_staff = is_staff
            # user.is_active = True
            user.last_login = now
            # user.date_joined = now
            # user.is_superuser = is_superuser
            user.save()
        return user



    def create_user(self, usuario, email, password=None, **extra_fields):
        return self._create_user(usuario, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, usuario, email, password, **extra_fields):
        return self._create_user(usuario, email, password, True, True,
                                 **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):

    usuario = models.CharField(_('Usuario'), max_length=60, unique=True)
    email = models.EmailField(null=True, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    # importante porque activaremos con confirmacion de correo de registro
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = CustomUserManager()
    # cuidado solo el inicio de sesion esta configurado con correo:
    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['email']
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return "%s - %s" %  (self.usuario, self.email)

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.usuario)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.usuario)    
        return (full_name.strip()) or u''

    def get_short_name(self):
        "Returns the short name for the user."
        return (self.usuario) or u''

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.usuario])


class Perfil_usuario(models.Model):
    """docstring for Perfil_usuario"""
    select_pais = (
        ('Peru', 'Perú'),
        ('Bolivia', 'Bolivia'),
        ('Chile', 'Chile'),
        ('Ecuador', 'Ecuador'),
        ('Colombia', 'Colombia'),
        ('Argentina', 'Argentina'),
        ('Brasil', 'Brasil'),
        ('Mexico', 'Mexico'),
        ('Otros', 'Otros')
    )

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    # dni = models.CharField(max_length=8, unique=True, null=True)
    nombres = models.CharField(max_length=120, null=True)
    apellidos = models.CharField(max_length=80, null=True)
    fecha_nacimiento = models.DateField(null=True,blank=True)
    sexo = models.CharField(choices=(('M', 'Masculino'), ('F', 'Femenino')),
                            max_length=20, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_usuarios',
                             default='fotos_usuarios/avatar.png', blank=True)
    celular = models.DecimalField(
        max_length=12, max_digits=12, decimal_places=0, null=True)
    codigo_pais = models.CharField(max_length=50, null=True, blank=True)
    pais = models.CharField(max_length=50, choices=select_pais, default='Peru', blank=True, null=True)
    ciudad = models.CharField(max_length=80, null=True)
    ocupacion = models.CharField(max_length=120, null=True, blank=True)
    profesion = models.CharField(max_length=120, null=True, blank=True)
    biografia = models.TextField(null=True, blank=True)
    sitio_web = models.URLField(null=True, blank=True)
    facebook= models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    empresa = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "%s - %s - %s" %  (self.nombres, self.apellidos, self.usuario.usuario ) or u''

    class Meta:
        verbose_name_plural = _('Perfil Usuarios')
        verbose_name = _('Perfil Usuario')
