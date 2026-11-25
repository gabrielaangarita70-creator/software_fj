# ============================================================
# Módulo: excepciones.py
# Propósito: definir las excepciones personalizadas del sistema
#            Software FJ. Todas heredan de SoftwareFJError para
#            poder capturarlas de forma genérica o específica.
# ============================================================


class SoftwareFJError(Exception):
    """Excepción base del sistema.

    Todas las excepciones propias heredan de esta clase, lo que
    permite capturar cualquier error del dominio con un solo
    'except SoftwareFJError' cuando no se necesita detalle.
    """

    def __init__(self, mensaje: str):
        # Se guarda el mensaje original del error.
        self.mensaje = mensaje
        # Se inicializa la clase padre Exception con ese mensaje,
        # para que str(error) devuelva el texto legible.
        super().__init__(mensaje)


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando un dato no cumple las validaciones.

    Ejemplos: nombre vacío, correo mal formado, teléfono con letras.
    """
    pass


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio.

    Ejemplo: crear una reserva sin cliente o sin servicio.
    """
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando el servicio no está disponible.

    Ejemplo: una sala que ya está reservada en ese horario.
    """
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando la operación no es válida para el estado actual.

    Ejemplo: cancelar una reserva que ya fue cancelada.
    """
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no cumple las reglas del negocio.

    Ejemplo: duración negativa o cero, o exceder el máximo permitido.
    """
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo produce un resultado imposible.

    Ejemplo: un costo total negativo por un descuento mal aplicado.
    """
    pass