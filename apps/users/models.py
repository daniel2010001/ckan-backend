from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """
    Administrador de modelos de usuario de CKAN personalizado.
    """

    def create_user(self, name: str, email: str, password: str, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name: str, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario de CKAN personalizado que utiliza el 'name'.
    """

    name = models.CharField("Nombre", max_length=30, unique=True, default="default")
    email = models.EmailField("Correo electrónico", unique=True)
    password = models.CharField("Contraseña", max_length=128)
    token = models.CharField("Clave API", max_length=255, null=False, blank=False)

    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado el", auto_now=True)
    deleted_at = models.DateTimeField("Eliminado el", null=True, blank=True)

    is_active = models.BooleanField("Activo", default=True)
    is_staff = models.BooleanField("Administrador", default=False)
    is_superuser = models.BooleanField("Superusuario", default=False)

    objects = UserManager()

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = ["email", "password", "token"]

    def __str__(self):
        return self.name
