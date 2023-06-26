import json
from django.shortcuts import render

class PantallaRtaOperador():
    def __init__(self, gestor):
        self.gestor = gestor

    def mostrarDatosLlamadaYValidacionRequerida(self, request, datos):
        """
        Muestra los datos de la llamada y la validación requerida en la pantalla principal.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.
            datos (dict): Datos de la llamada y la validación requerida.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        return render(request, "main.html" , {"datos":datos})

    def tomarIngresosDatosValidacion(self, request):
        """
        Toma los ingresos de datos de validación y llama al método para procesarlos.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse or bool: Respuesta HTTP o indicador de cancelación de llamada.
        """
        if request.method == "POST":
            validaciones = json.loads(request.body)
            return self.gestor.tomarDatosValidacion(validaciones, request) # Llamada al metodo 21

    def permitirIngresoRtaOperador(self, request):
        """
        Permite el ingreso de la respuesta del operador en la pantalla.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        return render(request, "rta_operador.html")

    def tomarIngresoRta(self, request):
        """
        Toma la respuesta del operador y llama al método correspondiente.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse or bool: Respuesta HTTP o indicador de cancelación de llamada.
        """
        if request.method == "POST":
            respuesta = json.loads(request.body)
            return self.gestor.tomarRtaOperador(request, respuesta) # Llamada al metodo 28

    def solicitarConfirmacion(self, request, respuesta):
        """
        Solicita la confirmación de la respuesta del operador en la pantalla.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.
            respuesta (str): Respuesta del operador.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        return render(request, "solicitar_confirmacion.html", {"respuesta":respuesta})

    def tomarConfirmacion(self, request):
        """
        Toma la confirmación de la respuesta del operador y llama al método correspondiente.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse or bool: Respuesta HTTP o indicador de cancelación de llamada.
        """
        if request.method == "POST":
            respuesta = json.loads(request.body)
            return self.gestor.confirmar(request, respuesta) # Llamada al metodo 31

    def informarAccionRegistrada(self, request):
        """
        Informa que la acción ha sido registrada en la pantalla.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        return render(request, "informacion_registrada.html")
    
    def ningunaSubopcion(self, request):
        """
        Muestra un mensaje de que no existe sub-opción para la opción seleccionada en la pantalla.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        return render(request, "home.html", {"motivo":"No existe sub-opción para la opción seleccionada."})
    
    def estaCancelada(self, request):
        """
        Verifica si la llamada ha sido cancelada.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            bool: Indicador de cancelación de llamada.
        """
        return self.gestor.llamadaEstaCancelada(request)
    
    def llamadaCancelada(self, request):
        """
        Muestra un mensaje de que la llamada ha sido cancelada en la pantalla.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        return render(request, "home.html", {"motivo":"El Cliente cuelga la llamada."})
    
    def cancelarLlamada(self, request):
        """
        Cancela la llamada y registra la acción de cancelación.

        Args:
            request (HttpRequest): Objeto de solicitud HTTP.

        Returns:
            HttpResponse: Respuesta HTTP.
        """
        return self.gestor.cancelarLlamada(request)
