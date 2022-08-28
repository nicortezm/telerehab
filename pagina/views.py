from django.shortcuts import render,redirect,reverse
from users import models
from . import forms
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from users.views import is_paciente,is_kinesiologo
from users.models import Kinesiologo


# Create your views here.

# VISTAS GENERICAS
def home(request):
    return render(request,'core/home.html') # El inicio es el login

def afterlogin_view(request):
    if is_paciente(request.user):      
        return redirect('paciente-dashboard')
                
    elif is_kinesiologo(request.user):

        accountapproval=Kinesiologo.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('kinesiologo-dashboard')
        else:
            return render(request,'pagina/kinesiologo_esperando_aprobacion.html')
    else:
        return redirect('admin-dashboard')


# VISTAS PACIENTE
def paciente_signup_view(request):
    # Asignamos los valores del formulario web al formulario django
    userForm=forms.UserForm() 
    pacienteForm=forms.PacienteForm()
    mydict={'userForm':userForm,'pacienteForm':pacienteForm} # Diccionario que retorna los valores 
    if request.method=='POST':
        userForm=forms.UserForm(request.POST)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save(commit=False) 
            user.username = user.email.replace('@','') # El username se genera a partir del email
            user.set_password(user.password)
            user.save()
            paciente=pacienteForm.save(commit=False)
            paciente.kinesiologo = Kinesiologo.objects.get(user_id=request.user.id)
            paciente.user=user
            paciente.save()
            my_paciente_group = Group.objects.get_or_create(name='PACIENTE') # Se crea o se asigna el grupo PACIENTE
            my_paciente_group[0].user_set.add(user) # Se añade el paciente al grupo
        return HttpResponseRedirect(reverse('kinesiologo-dashboard'))
    return render(request,'pagina/paciente_signup.html',context=mydict)


@login_required(login_url='login')
@user_passes_test(is_paciente)
def paciente_dashboard_view(request):
    return render(request,'pagina/paciente_dashboard.html')


# VISTAS KINESIOLOGO

def kinesiologo_signup_view(request):
    userForm=forms.UserForm()
    kinesiologoForm=forms.KinesiologoForm()
    mydict={'userForm':userForm,'kinesiologoForm':kinesiologoForm}
    if request.method=='POST':
        userForm=forms.UserForm(request.POST)
        kinesiologoForm=forms.KinesiologoForm(request.POST,request.FILES)
        if userForm.is_valid() and kinesiologoForm.is_valid():
            user=userForm.save(commit=False)
            user.username = user.email.replace('@','') # El username se genera a partir del email
            user.set_password(user.password)
            user.save()
            kinesiologo=kinesiologoForm.save(commit=False)
            kinesiologo.user=user
            kinesiologo.save()
            my_kinesiologo_group = Group.objects.get_or_create(name='KINESIOLOGO')
            my_kinesiologo_group[0].user_set.add(user)
        return HttpResponseRedirect(reverse('login'))
    return render(request,'pagina/kinesiologo_signup.html',context=mydict)    


@login_required(login_url='login')
@user_passes_test(is_kinesiologo)
def kinesiologo_dashboard_view(request):

 
    pacientes = models.Paciente.objects.filter(kinesiologo_id__user_id=request.user.id).values_list('comuna','telefono','cuidador')
    usuarios = list()
    for p in pacientes.values():
        
        usuario = models.User.objects.get(id=p['user_id'])
        p['first_name']= usuario.first_name
        p['last_name']=usuario.last_name
        usuarios.append(p)
    data = {
        'pacientes':usuarios,
        # 'users': users,
    }
    
    return render(request,'pagina/kinesiologo_dashboard.html',data)

@login_required(login_url='login')
@user_passes_test(is_kinesiologo)
def kinesiologo_esperando_view(request):
    return render(request,'pagina/kinesiologo_esperando_aprobacion.html')    