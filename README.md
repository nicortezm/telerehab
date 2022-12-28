# POMO Telerehabilitación

Plataforma virtual para la interacción entre paciente-kinesiologo. Esta aplicación nos permite realizar el seguimiento de rutinas de pacientes que no pueden asistir a centros de rehabilitación de forma presencial. 

La forma de demostración de avance de la terapia es a través de videos que, en primera instancia, sube el kinesiologo para un paciente, el cual debe replicar el ejercicio mostrado en el video y además debe adjuntar su evidencia para que luego el Kinesiologo a cargo pueda ver si está haciendo el ejercicio de forma correcta. 

Además ofrece multiples opciones de personalización de perfiles y de seguridad.

Indice
========

- [Instalación](#installation)
    - [Aplicación Principal](#typo3-extension-repository)
    - [Librerías de Python](#composer)
- [Archivos del proyecto](#typo3-setup)
    - [Módulos](#extension)
    - [Directorio de archivos](#database)
- [Manual de uso](#page-setup)
- [Requerimientos del proyecto](#license)


### Instalación
___
Stack tecnológico: Django + HTML + CSS + JS + SQLITE

#### **Aplicación Principal**

```shell 
Python > 4.0
```
La aplicación está hecha en Django, el framework más famoso de este lenguaje para el desarrollo web. Una vez instalado debemos seguir con la instalación de librerias.

Se puede obtener desde la página de Python.org

#### **Librerías de Python**

Las librerías de Python utilizadas se encuentran en el archivo requirements.txt el cual contiene lo siguiente:
```shell
asgiref==3.5.2
autopep8==1.7.0
Django==4.1.1
django-cleanup==6.0.0
numpy==1.23.3
opencv-python==4.6.0.66
Pillow==9.2.0
pycodestyle==2.9.1
sqlparse==0.4.2
toml==0.10.2
```
> **Cuidado**
> Se recomienda utilizar un entorno virtual donde instalar estas librerías.

Estas librerías pueden ser instaladas de forma automática, ubicandonos dentro del directorio de la aplicación y con el siguiente comando
```shell
pip install -r requirements.txt
```
Una vez instaladas las librerías podemos ejecutar el proyecto a través del siguiente comando:
```shell
python manage.py runserver
```
pueden haber variaciones, como por ejemplo de `python` a `python3`, pero el resto del comando queda igual.
### Archivos del proyecto
___

#### **Módulos**

La estructura del proyecto es modular. Los principales modulos son: `core` , `pagina` y `users`. Todos estos módulos están interconectados.

`core`: Módulo principal y desde el cual se hace el llamado a los demás modulos. Contiene configuraciones generales dentro del archivo `settings.py`

`pagina`: Módulo dedicado al flujo de datos dentro de la pagina web. Es el módulo más robusto y que contiene la mayor cantidad de lógica de programación.

`users`: Módulo de gestión de cuentas de usuario, perfiles, login y seguridad de la aplicación.

Otros archivos y carpetas:

`templates`: Contiene todas las plantilas hechas con django templates, con su respectivo lenguaje de etiquetas además de HTML y CSS.

`static`: Carpeta que almacena los archivos estáticos de la aplicación.

`media`: Carpeta que almacena los 'mediafiles' que se van cargando a la aplicacicón, tanto imagenes y videos. 

`requirements.txt`: Archivo que contiene los datos de las librerías de python necesarias para poder ejecutar el sistema.

#### **Arbol de archivos**

<br>

```shell
.
├── core
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pagina
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── users
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates
│   ├── core
│   │   ├── cambiar_contrasena.html
│   │   ├── footer.html
│   │   ├── home.html
│   │   ├── navbar.html
│   │   └── perfil.html
│   └── pagina
│       ├── admin_dashboard.html
│       ├── crear_categoria.html
│       ├── crear_ejercicio.html
│       ├── crear_kinesiologo.html
│       ├── crear_paciente.html
│       ├── crear_semana.html
│       ├── detalle_paciente.html
│       ├── gestion_kinesiologos.html
│       ├── kinesiologo_base.html
│       ├── kinesiologo_dashboard.html
│       ├── kinesiologo_feedback.html
│       ├── kinesiologo_lista_rutinas.html
│       ├── kinesiologo_lista_videos.html
│       ├── kinesiologo_ver_video.html
│       ├── logout.html
│       ├── modificar_ejercicio.html
│       ├── modificar_kinesiologo.html
│       ├── paciente_base.html
│       ├── paciente_comentarios.html
│       ├── paciente_dashboard.html
│       ├── paciente_ejercicio.html
│       ├── paciente_rutina.html
│       └── paciente_ver_feedback.html
├── static
├── media
├── manage.py
├── requirements.txt
└── db.sqlite3
```
### Manual de uso
___

#### **Administrador**

El usuario administrador es quien posee los maximos privilegios dentro de la aplicación. Este tipo de usuario tiene la capacidad de:

* Crear, modificar Usuarios del tipo Kinesiologo
* Modificar sus datos de usuario
* Crear, modificar Usuarios del tipo Paciente
* Crear, modificar, eliminar Categorías de Ejercicios
* Ver gráficos respecto a los tipos de usuarios registrados (Kinesiologo-Paciente)


#### **Kinesiologo**
* Crear, modificar Usuarios del tipo Paciente
* Modificar sus datos de usuario
* Crear Ejercicios
* Crear Semanas y rutinas de ejercicios
* Subir videos y Ver videos de pacientes
* Ver Comentarios y escribir feedback del ejercicio del paciente.


#### **Paciente**

* Modificar sus datos de usuario
* Ver ejercicios y rutinas asignadas
* Crear comentarios en los ejercicios y ver feedback

[Flujo explicado](POMO.pdf)

Playlist explicando el flujo -> proximamente. [WIP]



### Requerimientos del proyecto
___

- [x] RF001	Crear cuenta Usuario Médico
- [x] RF002	Crear cuenta Usuario Paciente
- [ ] RF003	Confirmación de Creación de Cuenta por Correo
- [x] RF004	Autenticación de Usuario
- [x] RF005	Modificación del Perfil Médico
- [x] RF006	Eliminar Perfil de Usuario Medico
- [x] RF007	Modificación del Perfil Paciente
- [x] RF008	Cargar Videos
- [ ] RF009	Descargar Videos
- [ ] RF010	Curva de avance
- [x] RF011	Ver Videos










