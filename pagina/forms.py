from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from users import models

class UserForm(forms.ModelForm):
    class Meta:
        model=models.User
        fields=['first_name','last_name','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class PacienteForm(forms.ModelForm):
    class Meta:
        model=models.Paciente
        fields=['description','cuidador','profile_pic','comuna','telefono']


class KinesiologoForm(forms.ModelForm):
    class Meta:
        model=models.Kinesiologo
        fields=['rut','profile_pic']




class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com', 'id': 'usuario','type':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'contrasena',
        }
))