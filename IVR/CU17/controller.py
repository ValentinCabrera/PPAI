from .models import Estado, Llamada, CategoriaLlamada, Cliente
from .views import PantallaRtaOperador

from datetime import datetime

class GestorAdmRtaOperador():
    enCurso = Estado
    datos = {}

    def __init__(self, llamada, categoria, opcion, sub_opcion):
        self.pantalla = PantallaRtaOperador(self)
        self.identificada = llamada
        self.catSeleccionada = categoria
        self.opcionSeleccionada = opcion
        self.seleccionada = sub_opcion

    def nuevaRtaOperador(self, request): 
        self.recibirLlamada() # Llamada al metodo 2
        self.obtenerDatosLlamada() # Llamada al metodo 8
        self.buscarValidaciones() # Llamada al metodo 14
        return self.pantalla.mostrarDatosLlamadaYValidacionRequerida(request, self.datos) # Llamada al metodo 19

    def recibirLlamada(self):
        self.buscarEstadoEnCurso() # Llamada al metodo 3
        fechaHoraActual = self.getFechaHoraActual() # Llamada al metodo 5
        self.identificada.derivarAOperador(self.enCurso, fechaHoraActual) # Llamada al metodo 6

    def getFechaHoraActual(self):
        return datetime.now()

    def buscarEstadoEnCurso(self):
        estados = Estado.objects.all()

        for i in estados:
            if i.esEnCurso(): # Llamada al metodo 4
                self.enCurso = i
                return

    def obtenerDatosLlamada(self):
        self.cliente, nombre = self.identificada.getNombreClienteLlamada() # Llamada al metodo 9

        descripcion_completa = self.catSeleccionada.getdescripcionCompletaCategoriaYOpcion() # Llamada al metodo 11

        self.datos["categoria"] = self.catSeleccionada.nombre
        self.datos["nombre_completo"] = nombre
        self.datos["descripcion_completa"] = descripcion_completa

    def buscarValidaciones(self):
        self.datos["validaciones"] = self.catSeleccionada.getValidaciones(self.opcionSeleccionada) # Llamada al metodo 15

    def tomarDatosValidacion(self, datos_validacion, request):
        datos_validacion = ["Berta", "¿Cual es el nombre de tu perro?"]
        return self.validarInformacionCliente(datos_validacion, request) # Llamada al metodo 22

    def validarInformacionCliente(self, datos_validacion, request):
        for i in datos_validacion:
            if not self.cliente.esInformacionCorrecta(datos_validacion): break # Llamada al metodo 23

        else:
            return self.pantalla.permitirIngresoRtaOperador(request) # Llamada al metodo 26

    def tomarRtaOperador(self, request):
        return self.pantalla.solicitarConfirmacion(request) # Llamada al metodo 29

    def confirmar(self, request):
        self.llamarCasoUso18() # Llamada al metodo 32
        
        try:
            return self.pantalla.informarAccionRegistrada(request) # Llamada al metodo 33
        
        except:
            pass

        finally:
            self.finalizarLlamada() # Llamada al metodo 34

    def llamarCasoUso18(self):
        pass

    def finalizarLlamada(self):
        self.buscarEstadoFinalizado() # Llamada al metodo 35
        fechaHoraActual = self.getFechaHoraActual() # Llamada al metodo 5

        self.identificada.finalizarLlamada(self.finalizada, fechaHoraActual) # Llamada al metodo 37
        self.finCU() # Llamada al metodo 40

    def buscarEstadoFinalizado(self):
        estados = Estado.objects.all()

        for i in estados:
            if i.esFinalizada(): # Llamada al metodo 36
                self.finalizada = i
                return 

    def finCU(self):
        pass