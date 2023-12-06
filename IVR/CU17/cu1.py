from CU17.models import (
    Llamada,
    CategoriaLlamada,
    OpcionLlamada,
    SubOpcionLlamada,
    Cliente,
    Iniciada)

def get_cliente():
    cliente = Cliente.objects.last()

    if not cliente:
        cliente = Cliente.objects.create(nombre_completo="Valentin Cabrerea")

    return cliente
def get_llamada():
    llamada = Llamada.objects.last()
    iniciada = Iniciada.objects.create()

    if not llamada:
        cliente = get_cliente()
        llamada = Llamada.objects.create(cliente=cliente, estadoActual=iniciada)

    else:
        llamada.estadoActual = iniciada
        llamada.save()

    return llamada
def get_categoria():
    categoria = CategoriaLlamada.objects.last()
    opcion = get_opcion()

    if not categoria:
        categoria = CategoriaLlamada.objects.create(nombre="Categoria 1", opcionSeleccionada=opcion)

    return categoria


def get_opcion():
    opcion = OpcionLlamada.objects.last()
    subOpcion = get_subOpcion()

    if not opcion:
        opcion = OpcionLlamada.objects.create(nombre="Opcion 1", seleccionada=subOpcion)

    return opcion


def get_subOpcion():
    subOpcion = SubOpcionLlamada.objects.last()

    if not subOpcion:
        subOpcion = SubOpcionLlamada.objects.create(nombre="Sub Opcion 1")

    return subOpcion