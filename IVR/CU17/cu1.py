from CU17.models import (
    Llamada,
    CategoriaLlamada,
    OpcionLlamada,
    SubOpcionLlamada,
    Cliente,
    Iniciada)

def get_cliente():
    """Retorna el ultimo cliente

    Returns:
        Objeto de tipo Cliente
    """
    cliente = Cliente.objects.last()

    if not cliente:
        cliente = Cliente.objects.create(nombre_completo="Valentin Cabrerea")

    return cliente
def get_llamada():
    """Busca la ultima llamada y el estado iniciada. 
    Si la llamada no existe la crea.
    En caso de que exista le asigna el estado.

    Returns:
        Objeto del tipo Llamada
    """
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
    """
    Obtiene la categoria
    Returns:
        Objeto de tipo CategoriaLlamada
    """
    categoria = CategoriaLlamada.objects.last()
    opcion = get_opcion()

    if not categoria:
        categoria = CategoriaLlamada.objects.create(nombre="Categoria 1", opcionSeleccionada=opcion)

    return categoria


def get_opcion():
    """_
    Obtiene la ultima opcion
    Returns:
        Objeto de tipo OpcionLlamada
    """
    opcion = OpcionLlamada.objects.last()
    subOpcion = get_subOpcion()

    if not opcion:
        opcion = OpcionLlamada.objects.create(nombre="Opcion 1", seleccionada=subOpcion)

    return opcion


def get_subOpcion():
    """
    Obtiene la ultima subOpcion
    Returns:
        Objeto de tipo SubOpcionLlamada
    """
    subOpcion = SubOpcionLlamada.objects.last()

    if not subOpcion:
        subOpcion = SubOpcionLlamada.objects.create(nombre="Sub Opcion 1")

    return subOpcion