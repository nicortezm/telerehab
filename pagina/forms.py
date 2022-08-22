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
        fields=['description','cuidador','profile_pic','comuna']


class KinesiologoForm(forms.ModelForm):
    class Meta:
        model=models.Kinesiologo
        fields=['rut','profile_pic']

