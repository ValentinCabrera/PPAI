from django.contrib import admin
from .models import Estado, Llamada, Cliente, CategoriaLlamada, OpcionLlamada, SubOpcionLlamada, Validacion

admin.site.register(Estado)
admin.site.register(Llamada)
admin.site.register(Cliente)
admin.site.register(CategoriaLlamada)
admin.site.register(OpcionLlamada)
admin.site.register(SubOpcionLlamada)
admin.site.register(Validacion)
