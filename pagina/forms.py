from django import forms
from users import models

class PacienteUserForm(forms.ModelForm):
    class Meta:
        model=models.User
        fields=['first_name','last_name','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class PacienteForm(forms.ModelForm):
    class Meta:
        model=models.Paciente
        fields=['description','cuidador','profile_pic']

class KinesiologoUserForm(forms.ModelForm):
    class Meta:
        model=models.User
        fields=['first_name','last_name','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class KinesiologoForm(forms.ModelForm):
    class Meta:
        model=models.Kinesiologo
        fields=['rut','profile_pic']

