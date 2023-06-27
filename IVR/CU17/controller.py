from .models import Estado, Llamada, CategoriaLlamada, Cliente
from .views import PantallaRtaOperador
from .cu28 import CU28

from datetime import datetime

class GestorAdmRtaOperador():
    enCurso = Estado
    datos = {}

    def __init__(self, llamada, categoria, opcion, sub_opcion):
        """
        Inicializa el Gestor de Administración de Respuestas del Operador.

        Args:
            llamada (Llamada): Llamada asociada.
            categoria (CategoriaLlamada): Categoría seleccionada.
            opcion (str): Opción seleccionada.
            sub_opcion (str): Subopción seleccionada.
        """
        self.pantalla = PantallaRtaOperador(self)
        self.identificada = llamada
        self.catSeleccionada = categoria
        self.opcionSeleccionada = opcion
        self.seleccionada = sub_opcion

    def nuevaRtaOperador(self, request): 
        """
        Procesa una nueva respuesta del operador.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        if self.seleccionada == None:
            return self.pantalla.ningunaSubopcion(request)
        
        if self.llamadaEstaCancelada(request):
            return self.llamadaEstaCancelada(request)

        self.recibirLlamada() # Llamada al metodo 2
        self.obtenerDatosLlamada() # Llamada al metodo 8
        self.buscarValidaciones() # Llamada al metodo 14
        return self.pantalla.mostrarDatosLlamadaYValidacionRequerida(request, self.datos) # Llamada al metodo 19

    def recibirLlamada(self):
        """
        Registra la recepción de la llamada.
        """
        self.buscarEstadoEnCurso() # Llamada al metodo 3
        fechaHoraActual = self.getFechaHoraActual() # Llamada al metodo 5
        self.identificada.derivarAOperador(self.enCurso, fechaHoraActual) # Llamada al metodo 6

    def getFechaHoraActual(self):
        """
        Obtiene la fecha y hora actual.

        Returns:
            datetime: Fecha y hora actual.
        """
        return datetime.now()

    def buscarEstadoEnCurso(self):
        """
        Busca y asigna el estado "EnCurso" al atributo enCurso.
        """
        estados = Estado.objects.all()

        for i in estados:
            if i.esEnCurso(): # Llamada al metodo 4
                self.enCurso = i
                return

    def obtenerDatosLlamada(self):
        """
        Obtiene los datos de la llamada y los asigna al atributo datos.
        """
        self.cliente, nombre = self.identificada.getNombreClienteLlamada() # Llamada al metodo 9

        descripcion_completa = self.catSeleccionada.getdescripcionCompletaCategoriaYOpcion() # Llamada al metodo 11

        self.datos["categoria"] = self.catSeleccionada.nombre
        self.datos["nombre_completo"] = nombre
        self.datos["descripcion_completa"] = descripcion_completa

    def buscarValidaciones(self):
        """
        Busca las validaciones correspondientes a la opción seleccionada y las asigna al atributo datos.
        """
        self.datos["validaciones"] = self.catSeleccionada.getValidaciones(self.opcionSeleccionada) # Llamada al metodo 15

    def tomarDatosValidacion(self, validaciones, request):
        """
        Toma los datos de validación y realiza la validación de la información del cliente.

        Args:
            validaciones (dict): Datos de validación del cliente.
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse or bool: Respuesta HTTP o indicador de cancelación de llamada.
        """
        if self.llamadaEstaCancelada(request):
            return self.llamadaEstaCancelada(request)
        
        return self.validarInformacionCliente(validaciones, request) # Llamada al metodo 22

    def validarInformacionCliente(self, datos_validacion, request):
        """
        Valida la información del cliente utilizando los datos de validación.

        Args:
            datos_validacion (dict): Datos de validación del cliente.
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse or None: Respuesta HTTP o None.
        """
        for pregunta, respuesta in datos_validacion.items():
            if not self.cliente.esInformacionCorrecta([pregunta, respuesta]): break # Llamada al metodo 23

        else:
            return self.pantalla.permitirIngresoRtaOperador(request) # Llamada al metodo 26
        
        # Flujo Alternativo 2
        from django.http import HttpResponse
        return HttpResponse(status=401) 

    def tomarRtaOperador(self, request, respuesta):
        """
        Toma la respuesta del operador y muestra una confirmación.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.
            respuesta (str): Respuesta del operador.

        Returns:
            HttpResponse or bool: Respuesta HTTP o indicador de cancelación de llamada.
        """
        if self.llamadaEstaCancelada(request):
            return self.llamadaEstaCancelada(request)

        return self.pantalla.solicitarConfirmacion(request, respuesta) # Llamada al metodo 29

    def confirmar(self, request, respuesta):
        """
        Confirma la respuesta del operador y finaliza la llamada si es necesario.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.
            respuesta (str): Respuesta del operador.

        Returns:
            HttpResponse or bool: Respuesta HTTP o indicador de cancelación de llamada.
        """
        if self.llamadaEstaCancelada(request):
            return self.llamadaEstaCancelada(request)

        if not self.llamarCasoUso18(respuesta): # Llamada al metodo 32
            # Flujo Alternativo 3
            return self.pantalla.permitirIngresoRtaOperador(request)

        try:
            return self.pantalla.informarAccionRegistrada(request) # Llamada al metodo 33
        
        except:
            pass

        finally:
            self.finalizarLlamada() # Llamada al metodo 34

    def llamarCasoUso18(self, respuesta):
        """
        Llama al caso de uso 28 para registrar una acción requerida.

        Args:
            respuesta (str): Respuesta del operador.

        Returns:
            bool: Indica si se pudo registrar la acción requerida.
        """
        cu28 = CU28()
        return True if cu28.registrarAccionRequerida(respuesta) else False

    def finalizarLlamada(self):
        """
        Finaliza la llamada y registra la acción de finalización.
        """
        self.buscarEstadoFinalizado() # Llamada al metodo 35
        fechaHoraActual = self.getFechaHoraActual() # Llamada al metodo 5

        self.identificada.finalizarLlamada(self.finalizada, fechaHoraActual) # Llamada al metodo 37
        self.finCU() # Llamada al metodo 40

    def buscarEstadoFinalizado(self):
        """
        Busca y asigna el estado "Finalizada" al atributo finalizada.
        """
        estados = Estado.objects.all()

        for i in estados:
            if i.esFinalizada(): # Llamada al metodo 36
                self.finalizada = i
                return 
            
    def finCU(self):
        """
        Realiza las acciones necesarias al finalizar el caso de uso.
        """

    # Flujo Alternativo 1

    def cancelarLlamada(self, request):
        """
        Cancela la llamada y registra la acción de cancelación.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        self.buscarEstadoCancelada()
        self.identificada.cancelarLlamada(self.cancelada, self.getFechaHoraActual())
        return self.pantalla.llamadaCancelada(request)

    def llamadaEstaCancelada(self, request):
        """
        Verifica si la llamada ha sido cancelada.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            bool: Indicador de cancelación de llamada.
        """
        self.buscarEstadoCancelada()
        if self.identificada.fuisteCancelada(self.cancelada):
            return self.pantalla.llamadaCancelada(request)

        return False

    def buscarEstadoCancelada(self):
        """
        Busca y asigna el estado "Cancelada" al atributo cancelada.
        """
        estados = Estado.objects.all()

        for i in estados:
            if i.esCancelada():
                self.cancelada = i
                return
