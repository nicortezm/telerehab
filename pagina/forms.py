from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm
from django import forms
from users import models
from pagina import models as pag_model


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'email', 'password']
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
        fields = ['rut', 'profile_pic', 'status']
        widgets = {
            'rut': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Ingrese Rut Kinesiologo'}
            ),
            'profile_pic': forms.FileInput(
                attrs={'type': 'file', 'id': 'file_upload_id', 'style': 'display: none;',
                       'accept': 'image/png, image/jpeg, image/JPG'}
            )
        }


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


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = pag_model.Categoria
        fields = ['nombre', 'descripcion']
        widgets = {'nombre': forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text',
                   'placeholder': 'Ingrese nombre categoria'}
        ), 'descripcion': forms.Textarea(
            attrs={'class': 'form-control',
                   'style': 'resize:none;', 'cols': '300', 'rows': '6'})}


class EjercicioForm(forms.ModelForm):
    class Meta:
        model = pag_model.Ejercicio
        fields = ['nombre', 'video', 'detalle', 'categoria']
        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text',
                       'placeholder': 'Ingrese nombre Ejercicio'}
            ), 'video': forms.FileInput(
                attrs={'type': 'file', 'id': 'file_upload_id', 'style': 'display: none;',
                       'accept': 'video/mp4,video/x-m4v,video/*'}
            ),
            'detalle': forms.Textarea(
                attrs={'class': 'form-control col-lg-6 col-sm-12 mt-2',
                       'style': 'resize:none;', 'cols': '10', 'rows': '10'}),
            'categoria': forms.Select(
                attrs={'class': 'form-control', 'name': 'cat', 'id': 'cat'}
            )
        }


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = models.User
        fields = ['first_name', 'email']


class UpdateKinesiologoForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'type': 'file', 'id': 'file_upload_id', 'style': 'display: none;',
               'accept': 'image/png, image/jpeg, image/JPG'}))

    telefono = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Kinesiologo
        fields = ['profile_pic']


class UpdatePacienteForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'type': 'file', 'id': 'file_upload_id', 'style': 'display: none;',
               'accept': 'image/png, image/jpeg, image/JPG'}))
    cuidador = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    comuna = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Paciente
        fields = ['profile_pic', 'cuidador',
                  'telefono', 'description', 'comuna']


class CreateSemanaForm(forms.ModelForm):

    class Meta:
        model = pag_model.Semana
        fields = ['nombre', ]
        widgets = {'nombre': forms.TextInput(
            attrs={'class': 'form-control', 'type': 'text',
                   'placeholder': 'Ingrese semana', 'form': 'formulario_categorias'}
        )}


class CreateGrabacionForm(forms.ModelForm):
    class Meta:
        model = pag_model.Grabacion
        fields = ['video']
        widgets = {
            'video': forms.FileInput(
                attrs={'type': 'file', 'id': 'file_upload_id', 'style': 'display: none;',
                       'accept': 'video/mp4,video/x-m4v,video/*'}
            )
        }
