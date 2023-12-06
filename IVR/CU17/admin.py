from django.contrib import admin
from .models import (Estado,
                     Llamada,
                     Cliente,
                     InformacionCliente,
                     CategoriaLlamada,
                     OpcionLlamada,
                     SubOpcionLlamada,
                     Validacion,
                     Iniciada,
                     EnCurso,
                     CambioEstado,
                     Cancelada)

admin.site.register(Estado)
admin.site.register(Iniciada)
admin.site.register(EnCurso)
admin.site.register(Cancelada)
admin.site.register(InformacionCliente)
admin.site.register(CambioEstado)
admin.site.register(Llamada)
admin.site.register(Cliente)
admin.site.register(CategoriaLlamada)
admin.site.register(OpcionLlamada)
admin.site.register(SubOpcionLlamada)
admin.site.register(Validacion)
