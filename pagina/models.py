from operator import truediv
from django.db import models
from users.models import Paciente, Kinesiologo
from django.core.validators import FileExtensionValidator
from django.utils import timezone
# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField("Nombre Categoría", max_length=50, unique=True)
    descripcion = models.TextField("Descripcion", max_length=500, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class Semana(models.Model):
    nombre = models.CharField("Nombre semana", max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):
    nombre = models.CharField("Nombre Ejercicio", max_length=50, unique=True)
    video = models.FileField(upload_to='videos/pomo', null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    detalle = models.TextField()
    date_uploaded = models.DateTimeField(default=timezone.now)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    kinesiologo = models.ForeignKey(
        Kinesiologo, on_delete=models.CASCADE, null=True)


class Actividad(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.PROTECT)
    kinesiologo = models.ForeignKey(Kinesiologo, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    semana = models.ForeignKey(Semana, on_delete=models.CASCADE)
    completado = models.BooleanField()


class Grabacion(models.Model):
    nombre = models.CharField("Nombre categoria", max_length=50, unique=True)
    video = models.FileField(upload_to='videos/pomo', null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    date_uploaded = models.DateTimeField(default=timezone.now)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)


class Feedback(models.Model):
    nota = models.IntegerField()  # TODO: ADD CHOICES
    comentario = models.TextField()
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
