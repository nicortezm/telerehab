from email.policy import default
from operator import truediv
from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField('email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Kinesiologo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/kinesiologo/', default="profile_pic/default.png", verbose_name="Foto de perfil")
    rut = models.CharField(max_length=9, null=False)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_email(self):
        return self.user.email

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/paciente/', default="profile_pic/default.png", verbose_name="Foto de perfil")
    description = models.TextField("descripcion", max_length=500, blank=True)
    cuidador = models.CharField(max_length=20, blank=True)
    telefono = models.IntegerField()
    comuna = models.CharField(max_length=30, blank=True)
    kinesiologo = models.ForeignKey(
        Kinesiologo, on_delete=models.PROTECT, blank=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name
