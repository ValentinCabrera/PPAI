from .models import Estado, Llamada, CategoriaLlamada, Cliente
from .views import PantallaRtaOperador
from .cu28 import CU28

from datetime import datetime

class GestorAdmRtaOperador():
    enCurso = Estado
    datos = {}

    def __init__(self):
        """
        Inicializa el Gestor de Administración de Respuestas del Operador.
        """
        self.pantalla = PantallaRtaOperador(self)

    def nuevaRtaOperador(self, request, llamada, categoria, opcion, sub_opcion):
        """
        Procesa una nueva respuesta del operador.

        Args:
            llamada (Llamada): Llamada asociada.
            categoria (CategoriaLlamada): Categoría seleccionada.
            opcion (str): Opción seleccionada.
            sub_opcion (str): Subopción seleccionada.
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        self.identificada = llamada
        self.catSeleccionada = categoria
        self.opcionSeleccionada = opcion
        self.seleccionada = sub_opcion

        if self.seleccionada == None:
            return self.pantalla.ningunaSubopcion(request)

        self.recibirLlamada()
        self.obtenerDatosLlamada()
        self.buscarValidaciones()
        return self.pantalla.mostrarDatosLlamadaYValidacionRequerida(request, self.datos)

    def recibirLlamada(self):
        """
        Registra la recepción de la llamada.
        """

        fechaHoraActual = self.getFechaHoraActual()
        self.identificada.derivarAOperador(fechaHoraActual)

    def getFechaHoraActual(self):
        """
        Obtiene la fecha y hora actual.

        Returns:
            datetime: Fecha y hora actual.
        """
        return datetime.now()

    def obtenerDatosLlamada(self):
        """
        Obtiene los datos de la llamada y los asigna al atributo datos.
        """
        self.cliente, nombre = self.identificada.getNombreClienteLlamada()

        descripcion_completa = self.catSeleccionada.getdescripcionCompletaCategoriaYOpcion(self.seleccionada)

        self.datos["categoria"] = self.catSeleccionada.nombre
        self.datos["nombre_completo"] = nombre
        self.datos["descripcion_completa"] = descripcion_completa

    def buscarValidaciones(self):
        """
        Busca las validaciones correspondientes a la opción seleccionada y las asigna al atributo datos.
        """
        self.datos["validaciones"] = self.catSeleccionada.getValidaciones(self.opcionSeleccionada, self.seleccionada)

    def tomarDatosValidacion(self, validaciones, request):
        """
        Toma los datos de validación y realiza la validación de la información del cliente.

        Args:
            validaciones (dict): Datos de validación del cliente.
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse or bool: Respuesta HTTP o indicador de cancelación de llamada.
        """
        
        return self.validarInformacionCliente(validaciones, request)

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
            if not self.cliente.esInformacionCorrecta([pregunta, respuesta]): break

        else:
            return self.pantalla.permitirIngresoRtaOperador(request)
        
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

        return self.pantalla.solicitarConfirmacion(request, respuesta)

    def confirmar(self, request, respuesta):
        """
        Confirma la respuesta del operador y finaliza la llamada si es necesario.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.
            respuesta (str): Respuesta del operador.

        Returns:
            HttpResponse or bool: Respuesta HTTP o indicador de cancelación de llamada.
        """

        if not self.llamarCasoUso18(respuesta):
            # Flujo Alternativo 3
            return self.pantalla.permitirIngresoRtaOperador(request)

        try:
            return self.pantalla.informarAccionRegistrada(request)
        
        except:
            pass

        finally:
            self.finalizarLlamada()

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

        fechaHoraActual = self.getFechaHoraActual()

        self.identificada.finalizarLlamada(fechaHoraActual)
        self.finCU()

    def finCU(self):
        """
        Realiza las acciones necesarias al finalizar el caso de uso.
        """
        pass