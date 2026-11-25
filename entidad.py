# ============================================================
# Módulo: entidad.py
# Propósito: definir la clase abstracta base del sistema.
#            Toda entidad del dominio (cliente, servicio, reserva)
#            hereda de aquí, cumpliendo el principio de abstracción.
# ============================================================

# Se importa ABC y abstractmethod para crear una clase abstracta
# real: no se puede instanciar y obliga a implementar sus métodos.
from abc import ABC, abstractmethod

# Se importa datetime para registrar la fecha de creación.
from datetime import datetime


class Entidad(ABC):
    """Clase abstracta que representa una entidad general del sistema.

    Al heredar de ABC, esta clase no puede instanciarse directamente:
    solo sirve como contrato para las clases derivadas.
    """
    def __init__(self, identificador: str, nombre: str):
        # Identificador único de la entidad (cédula, código, etc.).
        # Se valida que no venga vacío ni con solo espacios.
        if not identificador or not str(identificador).strip():
            # Se lanza ValueError porque es un fallo de programación
            # básico; las clases derivadas lo re-lanzarán como
            # excepción personalizada con contexto de negocio.
            raise ValueError("El identificador no puede estar vacío.")
        # Se valida también que el nombre tenga contenido.
        if not nombre or not str(nombre).strip():
            raise ValueError("El nombre no puede estar vacío.")
        # Se guarda el identificador ya limpio de espacios.
        self._identificador = str(identificador).strip()
        # Se guarda el nombre ya limpio de espacios.
        self._nombre = str(nombre).strip()
        # Se registra automáticamente la fecha y hora de creación.
        self._fecha_creacion = datetime.now()

    @property
    def nombre(self) -> str:
        """Devuelve el nombre en modo solo lectura (encapsulación)."""
        return self._nombre


    @property
    def identificador(self) -> str:
        """Devuelve el identificador en modo solo lectura (encapsulación)."""
        return self._identificador

    @property
    def fecha_creacion(self) -> datetime:
        """Devuelve la fecha de creación en modo solo lectura."""
        return self._fecha_creacion

    @abstractmethod
    def describir(self) -> str:
        """Método abstracto: cada entidad debe describirse a sí misma.

        Al ser abstracto, obliga a las clases derivadas a implementarlo,
        lo que habilita el polimorfismo más adelante.
        """
        # No se implementa aquí: las clases hijas lo sobrescriben.
        pass

    def __str__(self) -> str:
        """Representación legible de la entidad para imprimir en consola."""
        # Se usa el método abstracto describir(), demostrando polimorfismo.
        return self.describir()