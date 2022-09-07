from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.urls import path, reverse_lazy
from .forms import UserLoginForm
urlpatterns = [
    path('', LoginView.as_view(template_name='core/home.html',
         authentication_form=UserLoginForm, redirect_authenticated_user=True), name='login'),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('crear-paciente',
         views.paciente_signup_view, name='crear-paciente'),
    path('dashboard', views.paciente_dashboard_view,
         name='paciente-dashboard'),
    path('crear-kinesiologo', views.kinesiologo_signup_view,
         name='kinesiologosignup'),
    path('kinesiologo', views.kinesiologo_dashboard_view,
         name='kinesiologo-dashboard'),
    path('logout/', LogoutView.as_view(
        next_page=reverse_lazy('login')
    ), name='logout'),
    path('detalle_paciente/<id>/',
         views.detalle_paciente_view, name='detalle-paciente'),
    path('administrador/', views.admin_dashboard_view,
         name='admin-dashboard'),

]
