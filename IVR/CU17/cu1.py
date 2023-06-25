from CU17.models import Llamada, CategoriaLlamada, OpcionLlamada, SubOpcionLlamada

llamada = Llamada.objects.last()
categoria = CategoriaLlamada.objects.last()
opcion = OpcionLlamada.objects.last()
sub_opcion = SubOpcionLlamada.objects.last()