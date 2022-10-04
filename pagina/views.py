from django.shortcuts import render, redirect, reverse
from . import forms
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from users.views import is_paciente, is_kinesiologo, is_admin
from users.models import Kinesiologo, Paciente, User
from pagina.models import Categoria
# Create your views here.

# VISTAS GENERICAS


def home(request):
    return render(request, 'core/home.html')  # El inicio es el login


def afterlogin_view(request):

    if is_paciente(request.user):
        return redirect('paciente-dashboard')

    elif is_kinesiologo(request.user):
        return redirect('kinesiologo-dashboard')
    else:
        return redirect('admin-dashboard')


def perfil(request):
    if request.method == 'POST':
        user_form = forms.UpdateUserForm(request.POST)
        if is_kinesiologo(request.user):
            profile_form = forms.UpdateKinesiologoForm(
                request.POST, request.FILES)
        else:
            profile_form = forms.UpdatePacienteForm(
                request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(to='afterlogin')
    else:
        user_form = forms.UpdateUserForm(instance=request.user)
        if is_kinesiologo(request.user):
            profile_form = forms.UpdateKinesiologoForm()
        else:
            profile_form = forms.UpdatePacienteForm()
    return render(request, 'core/perfil.html')


# VISTAS PACIENTE


def paciente_signup_view(request):
    # Asignamos los valores del formulario web al formulario django
    userForm = forms.UserForm()
    pacienteForm = forms.PacienteForm()
    # Diccionario que retorna los valores
    mydict = {'userForm': userForm, 'pacienteForm': pacienteForm}
    if request.method == 'POST':
        userForm = forms.UserForm(request.POST)
        pacienteForm = forms.PacienteForm(request.POST, request.FILES)
        if userForm.is_valid() and pacienteForm.is_valid():
            user = userForm.save(commit=False)
            # El username se genera a partir del email
            user.username = user.email.replace('@', '')
            user.set_password(user.password)
            user.save()
            paciente = pacienteForm.save(commit=False)
            paciente.kinesiologo = Kinesiologo.objects.get(
                user_id=request.user.id)
            paciente.user = user
            paciente.save()
            my_paciente_group = Group.objects.get_or_create(
                name='PACIENTE')  # Se crea o se asigna el grupo PACIENTE
            # Se añade el paciente al grupo
            my_paciente_group[0].user_set.add(user)
        return HttpResponseRedirect(reverse('kinesiologo-dashboard'))
    return render(request, 'pagina/crear_paciente.html', context=mydict)


@login_required(login_url='login')
@user_passes_test(is_paciente)
def paciente_dashboard_view(request):
    return render(request, 'pagina/paciente_dashboard.html')


# VISTAS KINESIOLOGO

@login_required(login_url='login')
@user_passes_test(is_kinesiologo)
def kinesiologo_dashboard_view(request):

    pacientes = Paciente.objects.filter(
        kinesiologo_id__user_id=request.user.id).values_list('comuna', 'telefono', 'cuidador')
    usuarios = list()
    for p in pacientes.values():

        usuario = User.objects.get(id=p['user_id'])
        p['first_name'] = usuario.first_name
        p['last_name'] = usuario.last_name
        usuarios.append(p)
    data = {
        'pacientes': usuarios,
        # 'users': users,
    }

    return render(request, 'pagina/kinesiologo_dashboard.html', data)


@login_required(login_url='login')
@user_passes_test(is_kinesiologo)
def detalle_paciente_view(request, id):
    paciente = Paciente.objects.get(id=id)
    context = {
        'paciente': paciente
    }
    return render(request, 'pagina/detalle_paciente.html', context=context)


@login_required(login_url='login')
@user_passes_test(is_kinesiologo)
def crear_ejercicio_view(request):
    ejercicioForm = forms.EjercicioForm()
    if request.method == 'POST':
        ejercicioForm = forms.EjercicioForm(request.POST, request.FILES)
        if ejercicioForm.is_valid():
            ejercicio = ejercicioForm.save(commit=False)
            ejercicio.kinesiologo = Kinesiologo.objects.get(
                user__id=request.user.id)
            ejercicio.save()
        return HttpResponseRedirect(reverse('login'))

    context = {"ejercicioForm": ejercicioForm}
    return render(request, 'pagina/crear_ejercicio.html', context=context)

# VISTA ADMIN


@login_required(login_url='login')
@user_passes_test(is_admin)
def crear_kinesiologo(request):
    userForm = forms.UserForm()
    kinesiologoForm = forms.KinesiologoForm()
    mydict = {'userForm': userForm, 'kinesiologoForm': kinesiologoForm}
    if request.method == 'POST':
        userForm = forms.UserForm(request.POST)
        kinesiologoForm = forms.KinesiologoForm(request.POST, request.FILES)
        if userForm.is_valid() and kinesiologoForm.is_valid():
            user = userForm.save(commit=False)
            # El username se genera a partir del email de registro
            user.username = user.email.replace('@', '')
            user.set_password(user.password)
            user.save()
            kinesiologo = kinesiologoForm.save(commit=False)
            kinesiologo.user = user
            kinesiologo.save()
            my_kinesiologo_group = Group.objects.get_or_create(
                name='KINESIOLOGO')
            my_kinesiologo_group[0].user_set.add(user)
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'pagina/crear_kinesiologo.html', context=mydict)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    kinesiologos = Kinesiologo.objects.all()
    data = {
        'kinesiologos': kinesiologos
    }
    return render(request, 'pagina/admin_dashboard.html', data)


def crear_categoria_view(request):
    categoriaForm = forms.CategoriaForm()

    categorias = Categoria.objects.all()
    mydict = {'categoriaForm': categoriaForm, 'categorias': categorias}
    if request.method == 'POST':
        categoriaForm = forms.CategoriaForm(request.POST)
        if categoriaForm.is_valid():
            categoria = categoriaForm.save(commit=False)
            categoria.save()
        return HttpResponseRedirect(reverse('crear-categoria'))
    return render(request, 'pagina/crear_categoria.html', context=mydict)
