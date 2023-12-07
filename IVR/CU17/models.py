from django.db import models

class Iterador(): # Interfaz
    """Patron iterador"""
    def primero(self):
        pass
    def haTerminado(self):
        pass
    def actual(self):
        pass
    def siguiente(self):
        pass
class IteradorValidacion(Iterador):
    """Iterador concreto"""
    i = 0

    def __init__(self, elementos):
        """
        Constructor
        Args: Object[]
        """
        self.elementos = elementos
    def primero(self):
        """
        Setea el index a 0
        """
        self.i = 0

    def haTerminado(self):
        """
        Verifica si se finalizo el iterador
        Return: Boolean
        """
        return self.i == len(self.elementos)

    def actual(self):
        """
        Devuelve el elemento actual
        Return: Object
        """
        return self.elementos[self.i]

    def siguiente(self):
        """
        Incrementa el index
        """
        self.i += 1
class IAgregado():
    """
    Interfaz pora crear iterador
    """
    def crearIterador(self):
        pass
class OpcionLlamada(models.Model):
    nombre = models.CharField(max_length=30)

    def getDescripcionConSubOpcion(self, subOpcion):
        """
        Obtiene la descripción de la opción de llamada junto con la subopción seleccionada.

        Returns:
            descripcion (dict): Diccionario con la opción y la subopción seleccionada.
        """
        sub_opcion = subOpcion.getNombre()

        return {"opcion": self.nombre, "sub_opcion": sub_opcion}

    def getValidaciones(self, subOpcionSeleccionada):
        """
        Obtiene las validaciones asociadas a la opción de llamada.

        Returns:
            mensajes (list): Lista de mensajes de validación.
        """
        return subOpcionSeleccionada.getValidaciones()
class SubOpcionLlamada(models.Model, IAgregado):
    nombre = models.CharField(max_length=30)
    opcion = models.ForeignKey(OpcionLlamada, on_delete=models.RESTRICT)

    def getValidaciones(self):
        """
        Crea el iterador, lo recorre y retorna los mensajes de validacion
        Return:
            Array[String]: mensajes
        """
        iterador = self.crearIterador(self.validaciones.all())
        iterador.primero()

        mensajes = []

        while not iterador.haTerminado():
            actual = iterador.actual()
            mensajes.append(actual.getMensajeValidacion())
            iterador.siguiente()

        return mensajes

    def crearIterador(self, elementos):
        """
        Crea el iterador
        Args:
            elementos: Objects[]
        Return: Iterador()
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
class CategoriaLlamada(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    opcionSeleccionada = models.ForeignKey(OpcionLlamada, on_delete=models.RESTRICT)

    def getdescripcionCompletaCategoriaYOpcion(self, subOpcion):
        """
        Obtiene la descripción completa de la categoría de llamada y la opción seleccionada.

        Returns:
            descripcion (dict): Diccionario con la categoría y la opción seleccionada.
        """
        return self.opcionSeleccionada.getDescripcionConSubOpcion(subOpcion)

    def getValidaciones(self, opcionSeleccionada, subOpcionSeleccionada):
        """
        Obtiene las validaciones asociadas a la opción seleccionada de la categoría de llamada.

        Args:
            opcionSeleccionada (OpcionLlamada): Opción seleccionada.

        Returns:
            mensajes (list): Lista de mensajes de validación.
        """
        return opcionSeleccionada.getValidaciones(subOpcionSeleccionada)
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
    """
    Patron state
    Clase abstracta
    """
    def derivarAOperador(self, fechaHoraActual, llamada):
        pass

    def finalizarLlamada(self, fechaHoraActual, llamada, fechaHoraInicio):
        pass
class EnCurso(Estado):
    class Meta:
        proxy = True

    def finalizarLlamada(self, fechaHoraActual, llamada, fechaHoraInicio):
        """
        Finaliza la llamada creando el proximo cambio de estado, seteando el estado y calculando la duracion
        Args:
            fechaHoraActual: DataTime
            llamada: Llamada()
            fechaHoraInicio: DataTime
        """
        finalizada = self.crearProximoEstado()
        cambio = self.crearCambioEstado(fechaHoraActual, finalizada)

        llamada.agregarCambioEstado(cambio)
        llamada.setEstado(finalizada)

        duracion = self.calcularDuracion(fechaHoraInicio, fechaHoraActual)
        llamada.setDuracion(duracion)

    def calcularDuracion(self, fechaHoraInicio, fechaHoraActual):
        """
        Calcula la duración de la llamada.

        Args:
            fechaHoraInicio: DataTime
            fechaHoraActual: DataTime

        Return:
            duracion: Boolen
        """
        diferencia = fechaHoraActual - fechaHoraInicio
        tiempo = diferencia.total_seconds() / 60
        duracion = round(tiempo, 1)

        return duracion

    def crearProximoEstado(self):
        """
        Crea el proximo estado
        Return:
            finalizada: Finalizada()
        """

        finalizada = Finalizada.objects.create()
        return finalizada

    def crearCambioEstado(self, fechaHoraActual, estado):
        """
        Crea un cambio de estado
        Args:
            fechaHoraActual: DataTime
            estado: Estado()

        Return:
            cambio: CambioEstado()
        """
        cambio = CambioEstado.objects.create(estado=estado, fechaHoraInicio=fechaHoraActual)
        return cambio
class Cancelada(Estado):
    class Meta:
        proxy = True
class Finalizada(Estado):
    class Meta:
        proxy = True
class Correcta(Estado):
    class Meta:
        proxy = True
class Descartada(Estado):
    class Meta:
        proxy = True
class ConObservacion(Estado):
    class Meta:
        proxy = True
class AAuditar(Estado):
    class Meta:
        proxy = True
class Iniciada(Estado):
    class Meta:
        proxy = True
    def derivarAOperador(self, fechaHoraActual, llamada):
        """
        Deriva la llamda al operador, crea el cambio de estado y lo setea junto a su estado
        Args:
            fechaHoraActual: DataTime
            llamada: Llamada()
        """
        enCurso = self.crearProximoEstado()
        cambio = self.crearCambioEstado(fechaHoraActual, enCurso)

        llamada.agregarCambioEstado(cambio)
        llamada.setEstado(enCurso)

    def crearProximoEstado(self):
        """
        Crea el proximo estado
           Return:
               enCursi: EnCurso()
        """

        enCurso = EnCurso.objects.create()
        return enCurso

    def crearCambioEstado(self, fechaHoraActual, estado):
        """
        Crea un cambio de estado
        Args:
            fechaHoraActual: DataTime
            estado: Estado()

        Return:
            cambio: CambioEstado()
        """
        cambio = CambioEstado.objects.create(estado=estado, fechaHoraInicio=fechaHoraActual)
        return cambio
class Llamada(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    fechaHoraInicio = models.DateTimeField(auto_now=True)
    duracion = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    estadoActual = models.ForeignKey(Estado, on_delete=models.RESTRICT, related_name="llamada" ,related_query_name="estado")

    def derivarAOperador(self, fecha_hora):
        """
        Delega el cambio de estado al estado actual
        Args:
            fecha_hora: DataTime
        """
        self.estadoActual.derivarAOperador(fecha_hora, self)

    def getNombreClienteLlamada(self):
        """
        Obtiene el nombre del cliente asociado a la llamada.

        Returns:
            nombre_cliente (tuple): Nombre del cliente.
        """
        clienteDeLlamada = self.cliente
        return clienteDeLlamada, clienteDeLlamada.getNombre()

    def finalizarLlamada(self, fechaHoraActual):
        """
        Delega el comportamiento de finalizar llamada al estado actual
        Args:
            fechaHoraActual: DataTime
        """
        self.estadoActual.finalizarLlamada(fechaHoraActual, self, self.fechaHoraInicio)

    def agregarCambioEstado(self, cambio):
        """
        Agrega el cambio de estado a la llamada
        Args:
            cambio: CambioEstado
        """
        cambio.llamada = self
        cambio.save()

    def setEstado(self, estado):
        """
        Setea el estado
        Args:
            estado: Estado
        """
        self.estadoActual = estado
        self.save()

    def setDuracion(self, duracion):
        """
        Setea la duracion
        Args:
            duracion: Double
        """
        self.duracion = duracion
        self.save()
class CambioEstado(models.Model):
    llamada = models.ForeignKey(Llamada, on_delete=models.CASCADE, related_name="cambios_estado", null=True)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fechaHoraInicio = models.DateTimeField()
