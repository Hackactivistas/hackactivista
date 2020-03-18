from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import Usuario
from django.contrib.auth.backends import ModelBackend

# esto es sumamente importante, que nos va permitir iniciar por correo o usuario
# por defecto django tiene USERNAME_FIELD = 'usuario', basicamente para redes
# sociales es debe quedar aqui, y aqui forzamos que inice por email


class UsernameOrEmailBackend(ModelBackend):

    def authenticate(self, email=None, password=None, **kwargs):
        try:
            # autenticacion por usuario y email
            user = Usuario.objects.get(Q(usuario=email) | Q(email=email))
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            Usuario().set_password(password)
