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
                            CategoriaLlamada)

    info = InformacionCliente(id=0)
    cliente = Cliente(id=0, nombre_completo="Valentin Cabrera", informacion_cliente=info)
    llamada = Llamada(id=0, cliente=cliente)

    subopcion = SubOpcionLlamada(id=1, nombre="Subopcion 1")
    opcion = OpcionLlamada(id=0, nombre="Opcion 1", seleccionada=subopcion)
    categoria = CategoriaLlamada(nombre="Categoria 1", opcionSeleccionada=opcion)

    info.save()
    cliente.save()
    llamada.save()
    subopcion.save()
    opcion.save()
    categoria.save()

def create_states():
    start_apps()
    from CU17.models import Estado

    names = ["enCurso", "finalizada"]

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
