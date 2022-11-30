from django.shortcuts import render, redirect, reverse
from django.urls import is_valid_path
from . import forms
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from users.views import is_paciente, is_kinesiologo, is_admin, is_admin_or_kinesiologo
from users.models import Kinesiologo, Paciente, User
from pagina.models import Categoria, Ejercicio, Rutina, Semana
# Create your views here.

# VISTAS GENERICAS


@login_required(login_url='login')
def home(request):
    return render(request, 'core/home.html')  # El inicio es el login


def afterlogin_view(request):

    if is_paciente(request.user):
        return redirect('paciente-dashboard')

    elif is_kinesiologo(request.user):
        return redirect('kinesiologo-dashboard')
    else:
        return redirect('admin-dashboard')


@login_required(login_url='login')
def perfil(request):
    typeuser = ''
    user_form = forms.UpdateUserForm(instance=request.user)
    if is_kinesiologo(request.user):
        profile_form = forms.UpdateKinesiologoForm()
        typeuser = 'k'
    elif is_paciente(request.user):
        profile_form = forms.UpdatePacienteForm(instance=request.user.paciente)
        typeuser = 'p'
    else:
        profile_form = forms.UpdateUserForm()
        typeuser = 'a'

    if request.method == 'POST':
        user_form = forms.UpdateUserForm(request.POST, instance=request.user)
        if is_kinesiologo(request.user):
            profile_form = forms.UpdateKinesiologoForm(
                request.POST, request.FILES, instance=request.user.kinesiologo)
        elif is_paciente(request.user):
            profile_form = forms.UpdatePacienteForm(
                request.POST, request.FILES, instance=request.user.paciente)

        if user_form.is_valid():
            user_form.save()
            user_dummy = User.objects.get(id=request.user.id)
            user_dummy.username = user_form.cleaned_data['email'].replace(
                '@', '')
            user_dummy.save()
        if typeuser in ('p', 'k'):
            if profile_form.is_valid():
                profile_form.save()

        return redirect(to='afterlogin')
    mydict = {'userForm': user_form,
              'profileForm': profile_form, 'typeuser': typeuser}  #
    return render(request, 'core/perfil.html', context=mydict)


@login_required(login_url='login')
@user_passes_test(is_admin_or_kinesiologo)
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
    semanas = Semana.objects.filter(paciente_id__user_id=request.user.id)
    context = {'semanas': semanas}
    return render(request, 'pagina/paciente_dashboard.html', context)


# VISTAS KINESIOLOGO

@login_required(login_url='login')
@user_passes_test(is_admin_or_kinesiologo)
def kinesiologo_dashboard_view(request):
    if request.user.is_staff:
        pacientes = Paciente.objects.all().values_list('comuna', 'telefono', 'cuidador')
    else:
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
@user_passes_test(is_admin_or_kinesiologo)
def detalle_paciente_view(request, id):
    paciente = Paciente.objects.get(id=id)
    semana = Semana.objects.filter(paciente_id=id)
    context = {
        'paciente': paciente,
        'semanas': semana,
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


@login_required(login_url='login')
@user_passes_test(is_kinesiologo)
def modificar_ejercicio_view(request, id):
    ejercicio = Ejercicio.objects.get(id=id)
    ejercicioForm = forms.EjercicioForm(instance=ejercicio)
    if request.method == 'POST':
        ejercicioForm = forms.EjercicioForm(
            request.POST, request.FILES, instance=ejercicio)
        if ejercicioForm.is_valid():
            ejercicio = ejercicioForm.save(commit=False)
            ejercicio.save()
        return HttpResponseRedirect(reverse('mis-videos'))
    context = {"ejercicioForm": ejercicioForm,
               "ejercicio": ejercicio}
    return render(request, 'pagina/modificar_ejercicio.html', context=context)


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
def modificar_kinesiologo(request, id):
    kine = Kinesiologo.objects.get(id=id)
    usuario = User.objects.get(id=kine.user.id)
    userForm = forms.UpdateUserForm(instance=usuario)
    kinesiologoForm = forms.KinesiologoForm(instance=kine)
    mydict = {'userForm': userForm, 'kinesiologoForm': kinesiologoForm}
    if request.method == 'POST':
        userForm = forms.UpdateUserForm(
            request.POST, instance=usuario)
        kinesiologoForm = forms.KinesiologoForm(
            request.POST, instance=kine)
        if userForm.is_valid() and kinesiologoForm.is_valid():
            user = userForm.save(commit=False)
            # El username se genera a partir del email de registro
            user.username = user.email.replace('@', '')
            user.save()
            kinesiologo = kinesiologoForm.save(commit=False)
            kinesiologo.save()
        return HttpResponseRedirect(reverse('gestion-kinesiologos'))
    return render(request, 'pagina/modificar_kinesiologo.html', context=mydict)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    pacientes = Paciente.objects.all().count()
    kinesiologos = Kinesiologo.objects.all().count()
    data = {
        'kinesiologos': kinesiologos,
        'pacientes': pacientes
    }
    return render(request, 'pagina/admin_dashboard.html', data)


@login_required(login_url='login')
@user_passes_test(is_admin)
def crud_categoria_view(request):
    categoriaForm = forms.CategoriaForm()

    categorias = Categoria.objects.all()
    mydict = {'categoriaForm': categoriaForm, 'categorias': categorias}
    if request.method == 'POST':
        categoriaForm = forms.CategoriaForm(request.POST)
        if categoriaForm.is_valid():
            categoria = categoriaForm.save(commit=False)
            categoria.save()
        return HttpResponseRedirect(reverse('categorias'))
    return render(request, 'pagina/crear_categoria.html', context=mydict)


@login_required(login_url='login')
@user_passes_test(is_kinesiologo)
def crear_semana_view(request, id):
    createSemanaForm = forms.CreateSemanaForm()
    paciente = Paciente.objects.get(id=id)
    ejercicios = Ejercicio.objects.all()
    context = {
        'paciente': paciente,
        'ejercicios': ejercicios,
        'createSemanaForm': createSemanaForm
    }
    if request.method == 'POST':
        createSemanaForm = forms.CreateSemanaForm(request.POST)
        if createSemanaForm.is_valid():
            ejercicios = request.POST.getlist("checkEjercicio")
            semana = createSemanaForm.save(commit=False)
            semana.kinesiologo = Kinesiologo.objects.get(
                user_id=request.user.id)
            semana.paciente = Paciente.objects.get(id=id)
            semana.save()

            # Crear rutinas de semana
            for ejercicio in ejercicios:
                ejercicio_obj = Ejercicio.objects.get(id=ejercicio)
                rutina = Rutina.objects.create(
                    ejercicio=ejercicio_obj, semana=semana)
                rutina.save()
            return HttpResponseRedirect(reverse('detalle-paciente', kwargs={'id': semana.paciente.id}))
    return render(request, 'pagina/crear_semana.html', context=context)


@login_required(login_url='login')
@user_passes_test(is_kinesiologo)
def kinesiologo_mis_videos(request):
    ejercicios = Ejercicio.objects.filter(
        kinesiologo_id__user_id=request.user.id)
    # categorias = list(Categoria.objects.all().values_list('nombre', flat=True))

    categorias = set()
    for ejercicio in ejercicios:
        categorias.add(ejercicio.categoria.nombre)

    context = {
        'ejercicios': ejercicios,
        'categorias': categorias
    }
    return render(request, 'pagina/kinesiologo_lista_videos.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin_or_kinesiologo)
def gestion_kinesiologos(request):
    kinesiologos = Kinesiologo.objects.all()
    data = {
        'kinesiologos': kinesiologos
    }
    return render(request, 'pagina/gestion_kinesiologos.html', data)


@login_required(login_url='login')
@user_passes_test(is_kinesiologo)
def kinesiologo_rutinas(request, id):
    rutinas = Rutina.objects.filter(semana_id=id)

    semana = Semana.objects.get(id=id)
    print(rutinas)
    paciente = Paciente.objects.get(id=semana.paciente.id)
    data = {
        'rutinas': rutinas,
        'semana': semana,
        'paciente': paciente
    }
    return render(request, 'pagina/kinesiologo_lista_rutinas.html', data)


@login_required(login_url='login')
@user_passes_test(is_paciente)
def paciente_ejercicio(request, id):
    grabacionForm = forms.CreateGrabacionForm()
    rutina = Rutina.objects.get(id=id)
    ejercicio = Ejercicio.objects.get(id=rutina.ejercicio.id)
    semana = Semana.objects.get(id=rutina.semana.id)
    context = {
        "rutina": rutina,
        "ejercicio": ejercicio,
        "semana": semana,
        "grabacionForm": grabacionForm
    }
    if request.method == 'POST':
        grabacionForm = forms.CreateGrabacionForm(request.POST, request.FILES)
        if grabacionForm.is_valid():
            grabacion = grabacionForm.save(commit=False)
            grabacion.rutina = rutina

    return render(request, 'pagina/paciente_ejercicio.html', context=context)


@login_required(login_url='login')
@user_passes_test(is_paciente)
def paciente_rutina(request, id):
    rutinas = Rutina.objects.filter(semana_id=id)
    semana = Semana.objects.get(id=id)
    data = {
        'rutinas': rutinas,
        'semana': semana
    }
    return render(request, 'pagina/paciente_rutina.html', data)
