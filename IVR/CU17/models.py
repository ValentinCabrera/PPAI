from django.db import models


class SubOpcionLlamada(models.Model):
    nombre = models.CharField(max_length=30)

    def getValidaciones(self):
        validaciones = self.validaciones.all()
        mensajes = []
        
        for i in validaciones:
            mensajes.append(i.getMensajeValidacion()) # Llamada al metodo 18

        return mensajes

    def getNombre(self):
        return self.nombre

class OpcionLlamada(models.Model):
    nombre = models.CharField(max_length=30)
    seleccionada = models.ForeignKey(SubOpcionLlamada, on_delete=models.RESTRICT)

    def getDescripcionConSubOpcion(self):
        sub_opcion = self.seleccionada.getNombre() # Llamada al metodo 13
        return {"opcion":self.nombre, "sub_opcion":sub_opcion}

    def getValidaciones(self):
        return self.seleccionada.getValidaciones() # Llamada al metodo 17

class CategoriaLlamada(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    opcionSeleccionada = models.ForeignKey(OpcionLlamada, on_delete=models.RESTRICT)

    def getdescripcionCompletaCategoriaYOpcion(self):
        return self.opcionSeleccionada.getDescripcionConSubOpcion() # Llamada al metodo 12

    def getValidaciones(self, opcionSeleccionada):
        return opcionSeleccionada.getValidaciones() # Llamada al metodo 16


class Validacion(models.Model):
    sub_opcion = models.ForeignKey(SubOpcionLlamada, on_delete=models.RESTRICT, related_name="validaciones")
    nombre = models.CharField(max_length=150)

    def getMensajeValidacion(self):
        return self.nombre

class InformacionCliente(models.Model):
    validacion = models.ForeignKey(Validacion, on_delete=models.RESTRICT)
    datoAValidar = models.CharField(max_length=30)

    def esValidacion(self, validacion):
        return self.validacion.getMensajeValidacion() == validacion

    def esInformacionCorrecta(self, informacion):
        return self.datoAValidar == informacion

class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=30)
    informacion_cliente = models.ForeignKey(InformacionCliente, on_delete=models.RESTRICT)
    
    def getNombre(self):
        return (self, self.nombre_completo)
    
    def esInformacionCorrecta(self, datos_validacion):
        es_validacion = self.informacion_cliente.esValidacion(datos_validacion[1]) # Llamada al metodo 24
        es_informacion_correcta = self.informacion_cliente.esInformacionCorrecta(datos_validacion[0]) # Llamada al metodo 25
        return es_validacion and es_informacion_correcta


class Llamada(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)

    def derivarAOperador(self, estado, fecha_hora):
        enCurso = CambioEstado(llamada=self, estado=estado, fecha_hora=str(fecha_hora)) # Llamada al metodo 7
        enCurso.save()

    def getNombreClienteLlamada(self):
        clienteDeLlamada = self.cliente
        return clienteDeLlamada.getNombre() # Llamada al metodo 10

    def finalizarLlamada(self, estado, fecha_hora):
        CambioEstado(llamada=self, estado=estado, fecha_hora=str(fecha_hora)) # Llamada al metodo 38
        self.calcularDuracion() # Llamada al metodo 39

    def calcularDuracion(self):
        "caluclar duracion"

class Estado(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
   
    def esEnCurso(self):
        if self.name == "enCurso":
            return True
        
        return False

    def esFinalizada(self):
        if self.name == "finalizada":
            return True
        
        return False
    
    def __str__(self):
        return self.name

class CambioEstado(models.Model):
    llamada = models.ForeignKey(Llamada, on_delete=models.RESTRICT, related_name="cambios_estado")
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fecha_hora = models.DateTimeField()