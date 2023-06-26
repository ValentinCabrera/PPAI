#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def start_apps():
    import django
    from django.apps import apps
    from django.conf import settings

    if not apps.ready:
        django.setup()
        settings.INSTALLED_APPS 

def create_defaults():
    start_apps()
    from CU17.models import (InformacionCliente, 
                            Cliente, 
                            Llamada,
                            SubOpcionLlamada,
                            OpcionLlamada,
                            CategoriaLlamada,
                            Validacion, 
                            CambioEstado, 
                            Estado)
    
    from datetime import datetime

    sub_opcion = SubOpcionLlamada(id=0, nombre="Subopcion 1")
    opcion = OpcionLlamada(id=0, nombre="Opcion 1", seleccionada=sub_opcion)
    categoria = CategoriaLlamada(nombre="Categoria 1", opcionSeleccionada=opcion)
    cliente = Cliente(id=0, nombre_completo="Valentin Cabrera")

    validacion = Validacion(id=0, nombre="¿Cual es el nombre de tu perro?", sub_opcion=sub_opcion)
    info = InformacionCliente(id=0, validacion=validacion, datoAValidar="Berta", cliente=cliente)

    validacion2 = Validacion(id=1, nombre="¿En que universidad estudias?", sub_opcion=sub_opcion)
    info2 = InformacionCliente(id=1, validacion=validacion2, datoAValidar="UTN", cliente=cliente)

    llamada = Llamada(id=0, cliente=cliente)

    sub_opcion.save()
    opcion.save()
    categoria.save()
    validacion.save()
    validacion2.save()
    cliente.save()
    info.save()
    validacion2.save()
    info2.save()
    llamada.save()

    iniciada = Estado(name="EnCurso")
    cambio_estado = CambioEstado(llamada=llamada, estado=iniciada, fecha_hora=str(datetime.now()))
    cambio_estado.save()


def create_states():
    start_apps()
    from CU17.models import Estado

    names = ["Iniciada", "Cancelada", "EnCurso", "Finalizada"]

    for name in names:
        state = Estado(name)
        state.save()

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IVR.settings")

    if sys.argv[1] == "create_states":
        create_states()

    elif sys.argv[1] == "create_defaults":
        create_defaults()

    else:

        try:
            from django.core.management import execute_from_command_line

        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
