from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from .managers import UsuarioManager

class Usuario(models.Model):
    username =  models.CharField(max_length=255, unique=True)
    nombre = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = ['email']

    objects = UsuarioManager()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)
    
    @property
    def is_anonymous(self):
        return not self.is_authenticated

    @property
    def is_authenticated(self):
        return self.is_active

    def __str__(self):
        return self.email

class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique= True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Permiso(models.Model):
    nombre = models.CharField(max_length=100, unique= True )
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class UsuarioRol(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='roles', on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, related_name='usuarios', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'rol')

class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, related_name='permisos', on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, related_name='roles', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rol', 'permiso')

class UsuarioPermiso(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='permisos', on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, related_name='usuarios', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'permiso')

