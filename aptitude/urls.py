"""aptitude_crd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from rest_framework import routers
from aptitude_crd.views import *
from django.conf.urls.static import static
import django_dropimages

from django.urls import path
from django.conf import settings

app_name = 'aptitude'

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'cuestionarios', CuestionarioViewSet)
router.register(r'componentes', ComponenteViewSet)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('aviso-legal/', AvisoLegal.as_view(), name='aviso-legal'),
    path('proteccion-datos/', ProteccionDatos.as_view(), name='proteccion-datos'),
    path('terminos-condiciones/', TerminosCondiciones.as_view(), name='proteccion-datos'),
    path('gracias/', ThanksView.as_view(), name='gracias'),
    path('materiales/', MaterialesView.as_view(), name='materiales'),
    path('icope/', IcopeView.as_view(), name='icope'),

    path('registro/', RegistroView.as_view(), name='registro'),

    path('pacientes/', PacienteList.as_view(), name='paciente-lista'),
    path('pacientes/nuevo/', NuevoPaciente.as_view(), name='paciente-nuevo'),
    path('pacientes/buscar/', SearchView.as_view(), name='paciente-busqueda'),
    path('pacientes/buscar/<int:pk>/', PacienteCheck.as_view(), name='paciente-encontrado'),
    path('pacientes/<int:pk>/', PacienteUpdate.as_view(), name='paciente-detalle'),
    path('pacientes/<int:pk>/salud/', PacienteSalud.as_view(), name='paciente-salud'),
    path('pacientes/<int:pk>/visita/', create_visit_view, name='visita-nueva'),
    path('pacientes/<int:pk>/visitas/', PacienteVisitas.as_view(), name='visita-lista'),
    path('pacientes/<int:pk>/visitas/step_1/', create_visit_step_1, name='visita-step-1'),
    path('pacientes/<int:pk>/visitas/step_2/', create_visit_step_1, name='visita-step-2'),
    path('visita/<int:pk>/', VisitaDetail.as_view(), name='visita-detalle'),
    path('visita/<int:pk>/cerrar/', VisitaCierre.as_view(), name='visita-cerrar'),
    path('visita/<int:pk>/eval/', VisitaEval.as_view(), name='visita-eval'),
    path('visita/<int:pk>/step1/', VisitaEval1.as_view(), name='visita-eval-step-1'),
    path('screening/<int:pk>/', ScreeningView.as_view(), name='screening'),
    path('evaluacion/<int:pk>/', EvalView.as_view(), name='evaluacion'),

    path('descargas/', Descargas.as_view(), name='decargas'),
    path('descargas/registro/', download_registro, name='descargas-registro'),
    path('descargas/db/', download_db, name='descargas-db'),
    path('descargas/proxy/', download_proxy, name='descargas-proxy'),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/register/', AptitudeRegistrationView.as_view(), name='registration_register'),
    path('accounts/', include('registration.backends.admin_approval.urls')),
    path('logout/', LogoutView.as_view(), name='salir'),

    #AptitudeRegistrationView
    path('profile/', include('profile.urls', namespace='profile')),
    path('api/', include(router.urls)),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)