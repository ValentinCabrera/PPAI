from django.db import models

class InformacionCliente(models.Model):
    def esValidacion(validacion):
        return True

    def esInformacionCorrecta(informacion):
        return True

class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=30)
    informacion_cliente = models.ForeignKey(InformacionCliente, on_delete=models.RESTRICT)
    
    def getNombre(self):
        return self.nombre_completo
    
    def esInformacionCorrecta(self, datos_validacion):
        resultados = []

        for i in datos_validacion:
            resultados.append([self.informacion_cliente.esValidacion(i), self.informacion_cliente.esInformacionCorrecta(i)])

        return resultados


    def __str__(self):
        return self.nombre_completo

class Llamada(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)

    def tomadaPorOperador(self, estado, fecha_hora):
        CambioEstado(self, estado, fecha_hora)

    def getNombreClienteLlamada(self):
        nombre = self.cliente.getNombre()  
        return nombre

    def finalizarLlamada(self, estado, fecha_hora):
        CambioEstado(self, estado, fecha_hora)
        self.calcularDuracion()

    def calcularDuracion(self):
        "caluclar duracion"

class SubOpcionLlamada(models.Model):
    nombre = models.CharField(max_length=30)

    def getValidaciones(self):
        validaciones = self.validaciones.all()
        mensajes = []
        
        for i in validaciones:
            mensajes.append(i.getMensajeValidacion())


class OpcionLlamada(models.Model):
    nombre = models.CharField(max_length=30)
    seleccionada = models.ForeignKey(SubOpcionLlamada, on_delete=models.RESTRICT)

    def getDescripcionConSubOpcion(self):
        return self.nombre

    def getValidaciones(self):
        return self.seleccionada.getValidaciones()

class CategoriaLlamada(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True)
    opcionSeleccionada = models.ForeignKey(OpcionLlamada, on_delete=models.RESTRICT)

    def getdescripcionCompletaCategoriaYOpcion(self):
        return self.opcionSeleccionada

    def getValidaciones(self):
        return self.opcionSeleccionada.getValidaciones()


class Validacion(models.Model):
    sub_opcion = models.ForeignKey(SubOpcionLlamada, on_delete=models.RESTRICT, related_name="validaciones")
    audioMensajeValidacion = None

    def getMensajeValidacion(self):
        return self.audioMensajeValidacion

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
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)
    llamada = models.ForeignKey(Llamada, on_delete=models.RESTRICT, related_name="cambios_estado")
    fecha_hora = models.DateTimeField()