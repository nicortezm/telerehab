from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', LoginView.as_view(template_name='core/home.html'),name='login'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('paciente/signup', views.paciente_signup_view,name='pacientesignup'),
    path('paciente/dashboard', views.paciente_dashboard_view,name='paciente-dashboard'),
]
