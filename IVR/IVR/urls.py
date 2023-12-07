"""IVR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path

from CU17.controller import GestorAdmRtaOperador
from CU17.cu1 import *
from functools import partial

urlpatterns = []

gestor = GestorAdmRtaOperador()
pantalla = gestor.pantalla

urlpatterns = [
    path("admin/", admin.site.urls),
    path("mostrar/datos", partial(gestor.nuevaRtaOperador,
                                  llamada=get_llamada(),
                                  categoria=get_categoria(),
                                  opcion=get_opcion(),
                                  sub_opcion=get_subOpcion())), # Llamada al metodo 1
    path("tomar/ingreso/datos", pantalla.tomarIngresosDatosValidacion), # Llamada al metodo 20
    path("tomar/ingreso/rta", pantalla.tomarIngresoRta), # Llamada al metodo 27
    path("confirmar", pantalla.tomarConfirmacion),  # Llamada al metodo 30
]