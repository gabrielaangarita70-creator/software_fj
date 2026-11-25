# ============================================================
# Módulo: servicios.py
# Propósito: definir la clase abstracta Servicio y las tres
#            especializaciones (salas, equipos y asesorías),
#            aplicando herencia, polimorfismo y sobrecarga.
# ============================================================

# Se importa ABC y abstractmethod para obligar a las clases hijas
# a implementar ciertos métodos.
from abc import ABC, abstractmethod

# Se importa la clase base Entidad.
from entidad import Entidad

# Se importan las excepciones personalizadas del proyecto.
from excepciones import DatosInvalidosError, ServicioNoDisponibleError


class Servicio(Entidad, ABC):
    """Clase abstracta que representa cualquier servicio de Software FJ."""

    # IVA general aplicado a los servicios.
    IVA = 0.19

    def __init__(self, identificador: str, nombre: str, precio_base: float,
                 disponible: bool = True) -> None:
        # Se reutiliza la validación de la clase Entidad.
        super().__init__(identificador, nombre)
        # Se valida que el precio sea un número positivo.
        if not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise DatosInvalidosError(
                f"El precio base de '{nombre}' debe ser mayor que cero."
            )
        # Se guarda el precio en un atributo protegido.
        self._precio_base = float(precio_base)
        # Se guarda la disponibilidad del servicio.
        self._disponible = bool(disponible)

    @property
    def precio_base(self) -> float:
        """Devuelve el precio base del servicio."""
        return self._precio_base

    @property
    def disponible(self) -> bool:
        """Indica si el servicio puede reservarse."""
        return self._disponible

    def verificar_disponibilidad(self) -> None:
        """Lanza excepción si el servicio no está disponible."""
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' no está disponible."
            )

    # --------------------------------------------------------
    # Métodos sobrecargados para el cálculo de costos
    # --------------------------------------------------------
    def calcular_costo(self, cantidad: float = 1, impuesto: float = 0.0,
                       descuento: float = 0.0) -> float:
        """Variante 1: cálculo simple con impuesto y descuento opcionales."""
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser mayor que cero.")
        if not 0 <= descuento < 1:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 1.")
        subtotal = self._precio_base * cantidad
        total = subtotal * (1 - descuento) * (1 + impuesto)
        return round(total, 2)

    def calcular_costo_con_iva(self, cantidad: float, con_iva: bool) -> float:
        """Variante 2: cálculo indicando si se aplica IVA."""
        impuesto = self.IVA if con_iva else 0.0
        return self.calcular_costo(cantidad, impuesto)


    # --------------------------------------------------------
    # Métodos abstractos que deben sobrescribir las clases hijas
    # --------------------------------------------------------
    @abstractmethod
    def describir(self) -> str:
        """Devuelve la descripción del servicio."""
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, **parametros) -> None:
        """Valida los parámetros propios de cada servicio."""
        raise NotImplementedError


class ReservaSalas(Servicio):
    """Servicio de reserva de salas por horas."""

    def __init__(self, identificador: str, nombre: str, precio_base: float,
                 capacidad: int, disponible: bool = True) -> None:
        # Se llama al constructor de la clase abstracta.
        super().__init__(identificador, nombre, precio_base, disponible)
        # Se valida la capacidad de la sala.
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    @property
    def capacidad(self) -> int:
        """Devuelve la capacidad máxima de la sala."""
        return self._capacidad

    def describir(self) -> str:
        """Descripción legible del servicio de salas."""
        return (f"Sala '{self.nombre}' (ID {self.identificador}) | "
                f"Capacidad: {self._capacidad} personas | "
                f"Precio por hora: ${self._precio_base:,.0f}")

    def validar_parametros(self, **parametros) -> None:
        """Valida horas y número de asistentes."""
        # Se leen los parámetros con valores por defecto.
        horas = parametros.get("horas", 1)
        asistentes = parametros.get("asistentes", 1)
        # Se valida que las horas sean positivas.
        if horas <= 0:
            raise DatosInvalidosError("Las horas de reserva deben ser mayores que cero.")
        # Se valida que los asistentes no superen la capacidad.
        if asistentes > self._capacidad:
            raise DatosInvalidosError(
                f"La sala '{self.nombre}' admite máximo {self._capacidad} personas."
            )


class AlquilerEquipos(Servicio):
    """Servicio de alquiler de equipos por días."""

    def __init__(self, identificador: str, nombre: str, precio_base: float,
                 unidades: int, disponible: bool = True) -> None:
        # Se llama al constructor de la clase abstracta.
        super().__init__(identificador, nombre, precio_base, disponible)
        # Se valida el número de unidades disponibles.
        if not isinstance(unidades, int) or unidades < 0:
            raise DatosInvalidosError("Las unidades del equipo deben ser un entero no negativo.")
        self._unidades = unidades

    @property
    def unidades(self) -> int:
        """Devuelve cuántas unidades hay del equipo."""
        return self._unidades

    def describir(self) -> str:
        """Descripción legible del servicio de equipos."""
        return (f"Equipo '{self.nombre}' (ID {self.identificador}) | "
                f"Unidades: {self._unidades} | "
                f"Precio por día: ${self._precio_base:,.0f}")

    def validar_parametros(self, **parametros) -> None:
        """Valida días y cantidad de unidades solicitadas."""
        # Se leen los parámetros con valores por defecto.
        dias = parametros.get("dias", 1)
        cantidad = parametros.get("cantidad", 1)
        # Se valida que los días sean positivos.
        if dias <= 0:
            raise DatosInvalidosError("Los días de alquiler deben ser mayores que cero.")
        # Se valida que haya unidades suficientes.
        if cantidad > self._unidades:
            raise DatosInvalidosError(
                f"Solo hay {self._unidades} unidades disponibles de '{self.nombre}'."
            )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesorías especializadas por sesión."""

    def __init__(self, identificador: str, nombre: str, precio_base: float,
                 area: str, disponible: bool = True) -> None:
        # Se llama al constructor de la clase abstracta.
        super().__init__(identificador, nombre, precio_base, disponible)
        # Se valida que el área de la asesoría no esté vacía.
        if not isinstance(area, str) or len(area.strip()) < 3:
            raise DatosInvalidosError("El área de la asesoría debe tener al menos 3 caracteres.")
        self._area = area.strip()

    @property
    def area(self) -> str:
        """Devuelve el área de conocimiento de la asesoría."""
        return self._area

    def describir(self) -> str:
        """Descripción legible del servicio de asesorías."""
        return (f"Asesoría '{self.nombre}' (ID {self.identificador}) | "
                f"Área: {self._area} | "
                f"Precio por sesión: ${self._precio_base:,.0f}")

    def validar_parametros(self, **parametros) -> None:
        """Valida la duración de la sesión en horas."""
        # Se lee la duración con valor por defecto.
        duracion = parametros.get("duracion", 1)
        # Se valida que la duración sea razonable.
        if duracion <= 0:
            raise DatosInvalidosError("La duración de la asesoría debe ser mayor que cero.")
        if duracion > 8:
            raise DatosInvalidosError("Una asesoría no puede durar más de 8 horas.")