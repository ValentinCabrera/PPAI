from django.db import models

class SubOpcionLlamada(models.Model):
    nombre = models.CharField(max_length=30)

    def getValidaciones(self):
        """
        Obtiene las validaciones asociadas a la subopción de llamada.

        Returns:
            mensajes (list): Lista de mensajes de validación.
        """
        validaciones = self.validaciones.all()
        mensajes = []
        
        for i in validaciones:
            mensajes.append(i.getMensajeValidacion())

        return mensajes

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

class Llamada(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    fechaHoraInicio = models.DateTimeField(auto_now=True)
    duracion = models.DecimalField(decimal_places=1, max_digits=4, blank=True, null=True)

    def derivarAOperador(self, estado, fecha_hora):
        """
        Deriva la llamada a un operador.

        Args:
            estado (Estado): Estado de la llamada.
            fecha_hora (datetime): Fecha y hora de la derivación.
        """
        enCurso = CambioEstado(llamada=self, estado=estado, fechaHoraInicio=str(fecha_hora))
        enCurso.save()

    def getNombreClienteLlamada(self):
        """
        Obtiene el nombre del cliente asociado a la llamada.

        Returns:
            nombre_cliente (tuple): Nombre del cliente.
        """
        clienteDeLlamada = self.cliente
        return clienteDeLlamada, clienteDeLlamada.getNombre()

    def finalizarLlamada(self, estado, fecha_hora):
        """
        Finaliza la llamada.

        Args:
            estado (Estado): Estado de la llamada al finalizar.
            fecha_hora (datetime): Fecha y hora de finalización.
        """
        c = CambioEstado(llamada=self, estado=estado, fechaHoraInicio=str(fecha_hora))
        c.save()
        self.calcularDuracion(fecha_hora)

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

    def cancelarLlamada(self, estado, fecha_hora):
        """
        Cancela la llamada.

        Args:
            estado (Estado): Estado de la llamada al cancelar.
            fecha_hora (datetime): Fecha y hora de cancelación.
        """
        c = CambioEstado(llamada=self, estado=estado, fechaHoraInicio=str(fecha_hora))
        c.save()

    def fuisteCancelada(self, estado):
        """
        Verifica si la llamada fue cancelada.

        Args:
            estado (Estado): Estado de la llamada.

        Returns:
            fue_cancelada (bool): Indica si la llamada fue cancelada o no.
        """
        if self.cambios_estado.last().estado.nombre == "Cancelada":
            return True
        
        return False

class Estado(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
   
    def esEnCurso(self):
        """
        Verifica si el estado es "EnCurso".

        Returns:
            es_en_curso (bool): Indica si el estado es "EnCurso" o no.
        """
        if self.nombre == "EnCurso":
            return True
        
        return False

    def esFinalizada(self):
        """
        Verifica si el estado es "Finalizada".

        Returns:
            es_finalizada (bool): Indica si el estado es "Finalizada" o no.
        """
        if self.nombre == "Finalizada":
            return True
        
        return False
    
    def esCancelada(self):
        """
        Verifica si el estado es "Cancelada".

        Returns:
            es_cancelada (bool): Indica si el estado es "Cancelada" o no.
        """
        if self.nombre == "Cancelada":
            return True
        
        return False

class CambioEstado(models.Model):
    llamada = models.ForeignKey(Llamada, on_delete=models.RESTRICT, related_name="cambios_estado")
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fechaHoraInicio = models.DateTimeField()
