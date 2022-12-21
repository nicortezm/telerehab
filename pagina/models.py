from operator import truediv
from django.db import models
from users.models import Paciente, Kinesiologo
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from .utils import save_frame_from_video
import os
from django.conf import settings
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
    nombre = models.CharField("Nombre semana", max_length=50)
    kinesiologo = models.ForeignKey(
        Kinesiologo, on_delete=models.PROTECT, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):
    nombre = models.CharField("Nombre Ejercicio", max_length=50, unique=True)
    video = models.FileField(upload_to='videos/pomo', null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    video_thumbnail = models.ImageField(null=True)
    detalle = models.TextField()
    date_uploaded = models.DateTimeField(default=timezone.now)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    kinesiologo = models.ForeignKey(
        Kinesiologo, on_delete=models.CASCADE, null=True)

    def _set_thumbnail_source_image(self):
        # crear un thumbnail basado en el video
        image_path = os.path.splitext(self.video.path)[
            0] + '_thumbnail_src_image.jpg'
        # se puede reemplazar 0 con otro valor para las miniaturas
        save_frame_from_video(self.video.path, 0, image_path)

        # generar un path relativo a donde está el video
        media_image_path = os.path.relpath(image_path, settings.MEDIA_ROOT)

        self.video_thumbnail = media_image_path

    def save(self, *args, **kwargs):
        # si es que no hay miniatura asignada
        if not bool(self.video_thumbnail):
            # Tenemos que guardarlo primero, para que django genere el path para el video y luego ocuparlo para la minaturaf
            super().save(*args, **kwargs)
            self._set_thumbnail_source_image()

        super().save(*args, **kwargs)

    @property
    def get_category_name(self):
        return self.categoria.nombre


class Rutina(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)

    semana = models.ForeignKey(Semana, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    revisado = models.BooleanField(default=False)


class Grabacion(models.Model):
    video = models.FileField(upload_to='videos/pomo', null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    date_uploaded = models.DateTimeField(default=timezone.now, null=True)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, null=True)
    video_thumbnail = models.ImageField(null=True)

    def _set_thumbnail_source_image(self):
        # crear un thumbnail basado en el video
        image_path = os.path.splitext(self.video.path)[
            0] + '_thumbnail_src_image.jpg'
        # se puede reemplazar 0 con otro valor para las miniaturas
        save_frame_from_video(self.video.path, 0, image_path)

        # generar un path relativo a donde está el video
        media_image_path = os.path.relpath(image_path, settings.MEDIA_ROOT)

        self.video_thumbnail = media_image_path

    def save(self, *args, **kwargs):
        # si es que no hay miniatura asignada
        if not bool(self.video_thumbnail):
            # Tenemos que guardarlo primero, para que django genere el path para el video y luego ocuparlo para la minaturaf
            super().save(*args, **kwargs)
            self._set_thumbnail_source_image()

        super().save(*args, **kwargs)


class Feedback(models.Model):
    # nota = models.IntegerField()  # TODO: ADD CHOICES
    comentario = models.TextField()
    rutina = models.ForeignKey(
        Rutina, on_delete=models.CASCADE, null=True, blank=True)


class Comentario(models.Model):
    texto = models.TextField()
    rutina = models.ForeignKey(
        Rutina, on_delete=models.CASCADE, null=True, blank=True)
