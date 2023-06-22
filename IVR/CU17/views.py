from django.shortcuts import render

class PantallaRtaOperador():
    def mostrarDatosLlamadaYValidacionRequerida(self, gestor, request, datos):
        self.gestor = gestor
        return render(request, "main.html" , {"datos":datos})

    def tomarIngresosDatosValidacion(self, request):
        datos_validacion = request.data.get("datos_validacion")
        return self.gestor.tomarDatosValidacion(datos_validacion, request)

    def permitirIngresoRtaOperador(request):
        return render(request, "rta_operador.html")

    def tomarIngresoRta(self, request):
        return self.gestor.tomarRtaOperador(request)

    def solicitarConfirmacion(request):
        return render(request, "solicitar_confirmacion.html")

    def tomarConfirmacion(self, request):
            self.gestor.confirmar()

    def informarAccionRegistrada(request):
        return render(request, "informacion_registrada")
