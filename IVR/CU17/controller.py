from .models import Estado, Llamada, CategoriaLlamada, Cliente
from .views import PantallaRtaOperador

from datetime import datetime

class GestorAdmRtaOperador():
    llamada = Llamada.objects.last()
    catSeleccionada = CategoriaLlamada.objects.last()
    cliente = Cliente.objects.last()
    pantalla = PantallaRtaOperador()
    enCurso = Estado
    finalizada = Estado
    datos = {}

    def nuevaRtaOperador(self, request):
        self.recibirLlamada()
        self.obtenerDatosLlamada()
        self.buscarValidaciones()
        return self.pantalla.mostrarDatosLlamadaYValidacionRequerida(self, request, self.datos)

    def recibirLlamada(self):
        self.buscarEstadoEnCurso()
        fechaHoraActual = self.getFechaHoraActual()
        self.llamada.tomadaPorOperador(self.enCurso, fechaHoraActual)

    def getFechaHoraActual(self):
        return datetime.now

    def buscarEstadoEnCurso(self):
        estados = Estado.objects.all()

        for i in estados:
            if i.esEnCurso():
                self.enCurso = i
                return

    def obtenerDatosLlamada(self):
        nombre = self.llamada.getNombreClienteLlamada()
        descripcion_completa = self.catSeleccionada.getdescripcionCompletaCategoriaYOpcion()

        self.datos["categoria"] = self.catSeleccionada.nombre
        self.datos["nombre_completo"] = nombre
        self.datos["descripcion_completa"] = descripcion_completa

    def buscarValidaciones(self):
        self.datos["validaciones"] = self.catSeleccionada.getValidaciones()

    def tomarDatosValidacion(self, datos_validacion, request):
        resultados = self.cliente.esInformacionCorrecta(datos_validacion)

        if resultados:
            return self.pantalla.permitirIngresoRtaOperador(request)

    def validarInformacionCliente():
        pass

    def tomarRtaOperador(self, request):
        return self.pantalla.solicitarConfirmacion(request)

    def confirmar(self, request):
        self.llamarCasoUso18()
        try:
            return self.pantalla.informarAccionRegistrada(request)
        
        except:
            pass

        finally:
            self.finalizarLlamada()

    def llamarCasoUso18(self):
        pass

    def finalizarLlamada(self):
        self.buscarEstadoFinalizado()
        fechaHoraActual = self.getFechaHoraActual()

        self.llamada.finalizarLlamada(self.finalizada, fechaHoraActual)
        self.finCU()

    def buscarEstadoFinalizado(self):
        estados = Estado.objects.all()

        for i in estados:
            if i.esFinalizada():
                self.finalizada = i
                return 

    def finCU():
        pass