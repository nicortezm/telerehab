from tabnanny import verbose
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Paciente, Kinesiologo
from django.apps import AppConfig
# Register your models here.


admin.site.register(User, UserAdmin)
admin.site.register(Paciente)
admin.site.register(Kinesiologo)
