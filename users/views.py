from django.shortcuts import render

# Create your views here.


def is_kinesiologo(user):
    return user.groups.filter(name='KINESIOLOGO').exists()


def is_paciente(user):
    # retorna True si el usuario es PACIENTE y false en todos los otros casos
    return user.groups.filter(name='PACIENTE').exists()


def is_admin(user):
    return user.is_staff


def is_admin_or_kinesiologo(user):
    if user.groups.filter(name='KINESIOLOGO').exists() or user.is_staff:
        return True
    else:
        return False
