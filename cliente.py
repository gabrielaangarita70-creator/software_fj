# ============================================================
# Módulo: cliente.py
# Propósito: definir la clase Cliente con encapsulación de datos
#            personales y validaciones estrictas. Cada dato inválido
#            se reporta con una excepción personalizada y se registra
#            en el archivo de logs.
# ============================================================

# Se importa re para validar correo y teléfono con expresiones regulares.
import re

# Se importa la clase abstracta base.
from entidad import Entidad
# Se importan las excepciones personalizadas del sistema.
from excepciones import DatosInvalidosError
# Se importan las funciones de registro en el log.
from logger import registrar_info, registrar_error


class Cliente(Entidad):
    """Representa un cliente de Software FJ.

    Encapsula sus datos personales en atributos privados y solo
    permite modificarlos mediante propiedades con validación.
    """

    # Expresión regular sencilla para validar el formato del correo.
    PATRON_CORREO = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    # Expresión regular para teléfonos: solo dígitos, entre 7 y 10.
    PATRON_TELEFONO = r"^\d{7,10}$"

    def __init__(self, identificador: str, nombre: str,
                 correo: str, telefono: str):
        # Se inicializa la clase padre, que valida el identificador.
        # Si falla, se encadena como DatosInvalidosError (raise from).
        try:
         super().__init__(identificador, nombre)

        except ValueError as error:
            # Encadenamiento de excepciones: se conserva la causa original.
            raise DatosInvalidosError(
                f"Identificador de cliente inválido: {identificador}"
            ) from error

        # Se asignan los datos a través de las propiedades, de modo que
        # cada uno pase por su validación correspondiente.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        # Se registra la creación exitosa del cliente en el log.
        registrar_info(f"Cliente creado correctamente: {self._identificador}")

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del cliente."""
        # Se verifica que el nombre exista y no sea solo espacios.
        if not valor or not valor.strip():
            # Se registra el error antes de lanzar la excepción.
            registrar_error("Intento de crear cliente con nombre vacío.")
            # Se lanza la excepción personalizada de datos inválidos.
            raise DatosInvalidosError("El nombre del cliente no puede estar vacío.")
        # Se verifica que el nombre tenga al menos 3 caracteres.
        if len(valor.strip()) < 3:
            registrar_error(f"Nombre demasiado corto: '{valor}'.")
            raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres.")
        # Se verifica que solo contenga letras y espacios.
        if not all(parte.isalpha() for parte in valor.split()):
            registrar_error(f"Nombre con caracteres no permitidos: '{valor}'.")
            raise DatosInvalidosError("El nombre solo puede contener letras y espacios.")
        # Si pasó todas las validaciones, se guarda en formato título.
        self._nombre = valor.strip().title()

    @property
    def correo(self) -> str:
        """Devuelve el correo del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida y asigna el correo electrónico."""
        # Se comprueba que el correo no venga vacío.
        if not valor or not valor.strip():
            registrar_error("Intento de crear cliente con correo vacío.")
            raise DatosInvalidosError("El correo no puede estar vacío.")
        # Se valida el formato con la expresión regular de la clase.
        if not re.match(self.PATRON_CORREO, valor.strip()):
            registrar_error(f"Correo con formato inválido: '{valor}'.")
            raise DatosInvalidosError(f"El correo '{valor}' no tiene un formato válido.")
        # Se guarda el correo en minúsculas para uniformidad.
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Devuelve el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida y asigna el teléfono."""
        # Se convierte a texto por si llega como número.
        texto = str(valor).strip() if valor is not None else ""
        # Se valida que solo tenga dígitos y la longitud correcta.
        if not re.match(self.PATRON_TELEFONO, texto):
            registrar_error(f"Teléfono inválido: '{valor}'.")
            raise DatosInvalidosError(
                "El teléfono debe tener entre 7 y 10 dígitos numéricos."
            )
        # Se guarda el teléfono ya validado.
        self._telefono = texto

    def describir(self) -> str:
        """Implementa el método abstracto de Entidad.

        Devuelve una descripción legible del cliente.
        """
        # Se arma el texto con los datos encapsulados.
        return (f"Cliente [{self._identificador}] {self._nombre} | "
                f"Correo: {self._correo} | Teléfono: {self._telefono}")