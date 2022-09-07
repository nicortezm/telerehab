from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm
from django import forms
from users import models


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Ingrese contraseña', 'id': 'contrasena'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Ingrese nombre'}
            ),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese correo',
                       'id': 'usuario', 'type': 'email'}
            )
        }


class PacienteForm(forms.ModelForm):
    class Meta:
        model = models.Paciente
        fields = ['description', 'cuidador',
                  'profile_pic', 'comuna', 'telefono']
        widgets = {
            'cuidador': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Ingrese Cuidador'}
            ),
            'telefono': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Ingrese Numero Telefonico'}
            ),
            'comuna': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Ingrese Comuna'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'style': 'resize:none;', 'cols': '300', 'rows': '6'}
            ),
            'profile_pic': forms.FileInput(
                attrs={'type': 'file', 'id': 'file_upload_id', 'style': 'display: none;',
                       'accept': 'image/png, image/jpeg, image/JPG'}
            )
        }


class KinesiologoForm(forms.ModelForm):
    class Meta:
        model = models.Kinesiologo
        fields = ['rut', 'profile_pic']


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com',
               'id': 'usuario', 'type': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'contrasena',
        }
    ))


class UserChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)
    old_password = forms.CharField(label='Contraseña antigua', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
        }
    ))
    new_password1 = forms.CharField(label='Contraseña nueva', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
        }
    ))
    new_password2 = forms.CharField(label='Contraseña nueva (Confirmar)', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
        }
    ))
