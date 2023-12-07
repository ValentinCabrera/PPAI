from django.db import models



class Iterador():
    """
    Clase abstracta del iterador, la misma contiene los metodos vacios del metodo iterador, los cuales seran implementados por los iteradores concretos.
    """
    def primero(self):
        pass

    def haTerminado(self):
        pass

    def actual(self):
        pass

    def siguiente(self):
        pass
class IteradorValidacion(Iterador):
    """
        Clase IteradorValidacion, es una concrecion de la clase Iterador.
    """
    i = 0

    def __init__(self, elementos):
        """Constructor

        Args:
            elementos
        """
        self.elementos = elementos
    def primero(self):
        """
        Inicia el indicce en 0
        """
        self.i = 0

    def haTerminado(self):
        """
        Verifica si el iterador a terminado de recorrer todos los objetos
        Returns:
            Bool
        """
        return self.i == len(self.elementos)

    def actual(self):
        """
        Retorna el elemento actual que esta iterando
        Returns:
            elemento[i]
        """
        return self.elementos[self.i]

    def siguiente(self):
        """
        Aumenta el indice en 1
        """
        self.i += 1
class IAgregado():
    """
    Interfaz con el metodo necesario para crear un iterador, el mismo esta vacio
    """
    def crearIterador(self):
        pass

class SubOpcionLlamada(models.Model, IAgregado):
    nombre = models.CharField(max_length=30)

    def getValidaciones(self):
        """
        Obtiene las validaciones y utiliza un iterador para recorrerlas, guardando los mensajes en un array
        Returns:
            Lista de mensajes
        """
        iterador = self.crearIterador(self.validaciones.all())
        iterador.primero()

        mensajes = []

        if iterador.haTerminado() == False:
            actual = iterador.actual()
            mensajes.append(actual.getMensajeValidacion())
            iterador.siguiente()

        return mensajes

    def crearIterador(self, elementos):
        """
        Implementacion de la clase IAgregado
        Args:
            elementos

        Returns:
            iterador
        """
        iterador = IteradorValidacion(elementos)
        return iterador

    def getNombre(self):
        """
        Obtiene el nombre de la subopción de llamada.

        Returns:
            nombre (str): Nombre de la subopción de llamada.
        """
        return self.nombre

class OpcionLlamada(models.Model):
    nombre = models.CharField(max_length=30)
    seleccionada = models.ForeignKey(SubOpcionLlamada, on_delete=models.RESTRICT)

    def getDescripcionConSubOpcion(self):
        """
        Obtiene la descripción de la opción de llamada junto con la subopción seleccionada.

        Returns:
            descripcion (dict): Diccionario con la opción y la subopción seleccionada.
        """
        sub_opcion = self.seleccionada.getNombre()

        return {"opcion": self.nombre, "sub_opcion": sub_opcion}

    def getValidaciones(self):
        """
        Obtiene las validaciones asociadas a la opción de llamada.

        Returns:
            mensajes (list): Lista de mensajes de validación.
        """
        return self.seleccionada.getValidaciones()

class CategoriaLlamada(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    opcionSeleccionada = models.ForeignKey(OpcionLlamada, on_delete=models.RESTRICT)

    def getdescripcionCompletaCategoriaYOpcion(self):
        """
        Obtiene la descripción completa de la categoría de llamada y la opción seleccionada.

        Returns:
            descripcion (dict): Diccionario con la categoría y la opción seleccionada.
        """
        return self.opcionSeleccionada.getDescripcionConSubOpcion()

    def getValidaciones(self, opcionSeleccionada):
        """
        Obtiene las validaciones asociadas a la opción seleccionada de la categoría de llamada.

        Args:
            opcionSeleccionada (OpcionLlamada): Opción seleccionada.

        Returns:
            mensajes (list): Lista de mensajes de validación.
        """
        return opcionSeleccionada.getValidaciones()

class Validacion(models.Model):
    sub_opcion = models.ForeignKey(SubOpcionLlamada, on_delete=models.RESTRICT, related_name="validaciones")
    nombre = models.CharField(max_length=150)

    def getMensajeValidacion(self):
        """
        Obtiene el mensaje de validación.

        Returns:
            nombre (str): Mensaje de validación.
        """
        return self.nombre

class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=30)
    
    def getNombre(self):
        """
        Obtiene el nombre del cliente.

        Returns:
            nombre (str): Nombre del cliente.
        """
        return self.nombre_completo

    def esInformacionCorrecta(self, datos_validacion):
        """
        Verifica si la información del cliente es correcta basándose en las validaciones.

        Args:
            datos_validacion (tuple): Datos de validación (validacion, informacion).

        Returns:
            es_correcta (bool): Indica si la información es correcta o no.
        """
        informacion_cliente = self.informacion_cliente.all()

        for i in informacion_cliente:
            es_validacion = i.esValidacion(datos_validacion[0])
            es_informacion_correcta = i.esInformacionCorrecta(datos_validacion[1])

            if es_validacion and es_informacion_correcta:
                return True
            
        return False
        
class InformacionCliente(models.Model):
    validacion = models.ForeignKey(Validacion, on_delete=models.RESTRICT)
    datoAValidar = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, related_name="informacion_cliente")

    def esValidacion(self, validacion):
        """
        Verifica si la validación coincide con la validación de la información del cliente.

        Args:
            validacion (str): Validación a verificar.

        Returns:
            es_validacion (bool): Indica si la validación coincide o no.
        """
        return self.validacion.getMensajeValidacion() == validacion

    def esInformacionCorrecta(self, informacion):
        """
        Verifica si la información coincide con la información de la validación del cliente.

        Args:
            informacion (str): Información a verificar.

        Returns:
            es_correcta (bool): Indica si la información coincide o no.
        """
        return self.datoAValidar == informacion


class Estado(models.Model):
<<<<<<< Updated upstream
    def derivarAOperador(self, fechaHoraActual):
=======
    """
    Clase utilizada para la aplicacion del patron state
    """
    def derivarAOperador(self, fechaHoraActual, llamada):
>>>>>>> Stashed changes
        pass

    def finalizarLlamada(self, fechaHoraActual):
        pass

    def cancelarLlamada(self, fechaHoraActual):
        pass

    def crearEstadoCancelada(self):
        pass

    def esCancelada(self):
        pass


class EnCurso(Estado):
    """
    Concrecion de estado

    Args:
        Estado

    """
    class Meta:
        proxy = True
    def finalizarLlamada(self, fechaHoraActual):
        finalizada = self.crearProximoEstado()
        cambio = self.crearCambioEstado(fechaHoraActual, finalizada)

        self.llamada.first().agregarCambioEstado(cambio)
        self.llamada.first().setEstado(finalizada)

    def cancelarLlamada(self, fechaHoraActual):
        cancelada = self.crearEstadoCancelada()
        cambio = self.crearCambioEstado(fechaHoraActual, cancelada)

        self.llamada.first().agregarCambioEstado(cambio)
        self.llamada.first().setEstado(cancelada)

    def crearEstadoCancelada(self):
        cancelada = Cancelada.objects.create()
        return cancelada

    def crearProximoEstado(self):
        finalizada = Finalizada.objects.create()
        return finalizada

    def crearCambioEstado(self, fechaHoraActual, estado):
        cambio = CambioEstado.objects.create(estado=estado, fechaHoraInicio=fechaHoraActual)
        return cambio

class Cancelada(Estado):
    """
    Concrecion de estado

    Args:
        Estado

    """
    class Meta:
        proxy = True
    def esCancelada(self):
        return True

class Finalizada(Estado):
    """
    Concrecion de estado

    Args:
        Estado

    """
    class Meta:
        proxy = True

class Iniciada(Estado):
    """
    Concrecion de estado

    Args:
        Estado

    """
    class Meta:
        proxy = True
<<<<<<< Updated upstream
    def derivarAOperador(self, fechaHoraActual):
=======
    def derivarAOperador(self, fechaHoraActual, llamada):
        """
        Metodo 5
        """
>>>>>>> Stashed changes
        enCurso = self.crearProximoEstado()
        cambio = self.crearCambioEstado(fechaHoraActual, enCurso)

        self.llamada.first().agregarCambioEstado(cambio)
        self.llamada.first().setEstado(enCurso)

    def cancelarLlamada(self, fechaHoraActual):
        cancelada = self.crearEstadoCancelada()
        cambio = self.crearCambioEstado(fechaHoraActual, cancelada)

        self.llamada.first().agregarCambioEstado(cambio)
        self.llamada.first().setEstado(cancelada)

    def crearEstadoCancelada(self):
        cancelada = Cancelada.objects.create()
        return cancelada

    def crearProximoEstado(self):
        """
        Metodo 6

        Returns:
            estado EnCurso
        """
        enCurso = EnCurso.objects.create() #Metodo 7
        return enCurso

    def crearCambioEstado(self, fechaHoraActual, estado):
        """
        Metodo 8

        Returns:
            Cambio de Estado
        """
        cambio = CambioEstado.objects.create(estado=estado, fechaHoraInicio=fechaHoraActual)#Metodo 9
        return cambio

    def __str__(self):
        return "Iniciada"

class Llamada(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    fechaHoraInicio = models.DateTimeField(auto_now=True)
    duracion = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    estadoActual = models.ForeignKey(Estado, on_delete=models.RESTRICT, related_name="llamada" ,related_query_name="estado")

    def derivarAOperador(self, fecha_hora):
        self.estadoActual.derivarAOperador(fecha_hora)

    def getNombreClienteLlamada(self):
        """
        Metodo 13
        Obtiene el nombre del cliente asociado a la llamada.

        Returns:
            nombre_cliente (tuple): Nombre del cliente.
        """
        clienteDeLlamada = self.cliente
        return clienteDeLlamada, clienteDeLlamada.getNombre()

    def finalizarLlamada(self, fechaHoraActual):
        self.estadoActual.finalizarLlamada(fechaHoraActual)
        self.calcularDuracion(fechaHoraActual)

    def calcularDuracion(self, fin):
        """
        Calcula la duración de la llamada.

        Args:
            fin (datetime): Fecha y hora de finalización de la llamada.
        """
        diferencia = fin - self.fechaHoraInicio
        tiempo = diferencia.total_seconds() / 60
        self.duracion = round(tiempo, 1)
        self.save()

    def cancelarLlamada(self, fecha_hora):
        self.estadoActual.cancelarLlamada(fecha_hora)

    def fuisteCancelada(self):
        """
        Verifica si la llamada fue cancelada.

        Args:
            estado (Estado): Estado de la llamada.

        Returns:
            fue_cancelada (bool): Indica si la llamada fue cancelada o no.
        """
        return self.estadoActual.esCancelada()

    def agregarCambioEstado(self, cambio):
        """
        Metodo 10
        """
        cambio.llamada = self
        cambio.save()

    def setEstado(self, estado):
        """
        Metodo 11
        """
        self.estadoActual = estado
        self.save()

class CambioEstado(models.Model):
    llamada = models.ForeignKey(Llamada, on_delete=models.CASCADE, related_name="cambios_estado", null=True)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fechaHoraInicio = models.DateTimeField()
