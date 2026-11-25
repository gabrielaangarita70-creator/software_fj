# ============================================================
# Módulo: reservas.py
# Propósito: integrar cliente y servicio en una reserva,
#            encadenando validaciones y excepciones.
# ============================================================

from datetime import datetime

from cliente import Cliente
from excepciones import DatosInvalidosError, ServicioNoDisponibleError
from logger import registrar_info  # ajusta al nombre real de tu función
from servicios import Servicio


class Reserva:
    """Representa la reserva de un servicio por parte de un cliente."""

    def __init__(self, cliente: Cliente, servicio: Servicio,
                 cantidad: float, con_iva: bool = True, **parametros) -> None:
        # Se valida que los objetos recibidos sean del tipo esperado.
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("La reserva requiere un servicio válido.")
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise DatosInvalidosError("La cantidad de la reserva debe ser mayor que cero.")

        # Se verifica disponibilidad y se encadena la causa original.
        try:
            servicio.verificar_disponibilidad()
        except ServicioNoDisponibleError as error:
            raise DatosInvalidosError(
                f"No se pudo reservar '{servicio.nombre}': {error}"
            ) from error

        # Se validan los parámetros propios del servicio.
        try:
            servicio.validar_parametros(**parametros)
        except DatosInvalidosError as error:
            raise DatosInvalidosError(
                f"Parámetros inválidos para '{servicio.nombre}': {error}"
            ) from error

        self._cliente = cliente
        self._servicio = servicio
        self._cantidad = cantidad 
        self._parametros = parametros
        self._fecha = datetime.now()
        self._estado = "PENDIENTE"
        self._con_iva = con_iva

    @property
    def costo_total(self) -> float:
        """Costo de la reserva con segun se aplique IVA o no."""
        return self._servicio.calcular_costo_con_iva(self._cantidad, self._con_iva)

    def confirmar(self) -> None:
        """Marca la reserva como confirmada y la registra en el log."""
        self._estado = "CONFIRMADA"
        registrar_info(f"Reserva confirmada: {self.describir()}")

    def describir(self) -> str:
        """Resumen legible de la reserva."""
        return (f"{self._cliente.nombre} reservó {self._servicio.nombre} "
                f"({self._cantidad}) | Total: ${self.costo_total:,.0f} | "
                f"Estado: {self._estado}")