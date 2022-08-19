from django.shortcuts import render,redirect,reverse
from users import models
from . import forms
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.

def home(request):
  return render(request,'core/home.html')


def paciente_signup_view(request):
    userForm=forms.PacienteUserForm()
    pacienteForm=forms.PacienteForm()
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save(commit=False)
            user.username = user.email.replace('@','')
            user.set_password(user.password)
            user.save()
            paciente=pacienteForm.save(commit=False)
            paciente.user=user
            paciente.save()
            my_paciente_group = Group.objects.get_or_create(name='PACIENTE')
            my_paciente_group[0].user_set.add(user)
        return HttpResponseRedirect('login')
    return render(request,'pagina/paciente_signup.html',context=mydict)

def is_paciente(user):
    return user.groups.filter(name='PACIENTE').exists()

@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_dashboard_view(request):
    return render(request,'pagina/paciente_dashboard.html')


def is_kinesiologo(user):
    return user.groups.filter(name='KINESIOLOGO').exists()

def afterlogin_view(request):
    if is_paciente(request.user):      
        return redirect('paciente-dashboard')
                
    elif is_kinesiologo(request.user):

        return redirect('kinesiologo-dashboard')

        # accountapproval=KMODEL.Kinesiologo.objects.all().filter(user_id=request.user.id,status=True)
        # if accountapproval:
        #     return redirect('kinesiologo/kinesiologo-dashboard')
        # else:
        #     return render(request,'kinesiologo/kinesiologo_esperando_aprobacion.html')
    else:
        return redirect('admin-dashboard')