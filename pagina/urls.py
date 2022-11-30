from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy
from .forms import UserLoginForm, UserChangePasswordForm
urlpatterns = [
    path('', LoginView.as_view(template_name='core/home.html',
         authentication_form=UserLoginForm, redirect_authenticated_user=True), name='login'),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('crear-paciente',
         views.paciente_signup_view, name='crear-paciente'),
    path('dashboard', views.paciente_dashboard_view,
         name='paciente-dashboard'),
    path('crear-kinesiologo', views.crear_kinesiologo,
         name='crear-kinesiologo'),
    path('crear-kinesiologo/<id>', views.modificar_kinesiologo,
         name='modificar-kinesiologo'),
    path('kinesiologo', views.kinesiologo_dashboard_view,
         name='kinesiologo-dashboard'),
    path('logout/', LogoutView.as_view(
        next_page=reverse_lazy('login')
    ), name='logout'),
    path('detalle_paciente/<id>/',
         views.detalle_paciente_view, name='detalle-paciente'),
    path('administrador/', views.admin_dashboard_view,
         name='admin-dashboard'),
    path('cambiar-contrasena', PasswordChangeView.as_view(
        template_name='core/cambiar_contrasena.html', success_url='/', form_class=UserChangePasswordForm), name='cambiar-contrasena'),
    path('perfil', views.perfil, name='perfil'),
    path('crear-ejercicio', views.crear_ejercicio_view,
         name='crear-ejercicio'),
    path('categorias', views.crud_categoria_view,
         name='categorias'),
    path('detalle_paciente/<id>/crear-semana/',
         views.crear_semana_view, name='crear-semana'),
    path('mis-videos', views.kinesiologo_mis_videos, name='mis-videos'),
    path('gestion-kinesiologos', views.gestion_kinesiologos,
         name='gestion-kinesiologos'),
    path('detalle_paciente/semana/<id>',
         views.kinesiologo_rutinas, name="detalle-rutina"),
    path('modificar-ejercicio/<id>', views.modificar_ejercicio_view,
         name="modificar-ejercicio"),
    path('ejercicios/<id>', views.paciente_ejercicio, name="paciente-ejercicio"),
    path('semana/<id>', views.paciente_rutina, name="paciente-rutina"),
    path('comentarios/<id>', views.paciente_comentarios,
         name="paciente-comentarios"),

]
