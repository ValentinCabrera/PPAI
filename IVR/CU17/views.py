from django.shortcuts import render

class PantallaRtaOperador():
    def __init__(self, gestor):
        self.gestor = gestor

    def mostrarDatosLlamadaYValidacionRequerida(self, request, datos):
        return render(request, "main.html" , {"datos":datos})

    def tomarIngresosDatosValidacion(self, request):

        datos = "Berta"
        return self.gestor.tomarDatosValidacion(datos, request) # Llamada al metodo 21

    def permitirIngresoRtaOperador(self, request):
        return render(request, "rta_operador.html")

    def tomarIngresoRta(self, request):
        return self.gestor.tomarRtaOperador(request) # Llamada al metodo 28

    def solicitarConfirmacion(self, request):
        return render(request, "solicitar_confirmacion.html")

    def tomarConfirmacion(self, request):
            return self.gestor.confirmar(request) # Llamada al metodo 31

    def informarAccionRegistrada(self, request):
        return render(request, "informacion_registrada.html")
