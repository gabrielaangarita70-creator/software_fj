# ============================================================
# Módulo: logger.py
# Propósito: registrar todos los eventos y errores del sistema
#            en un archivo de texto (logs/eventos.log), sin usar
#            base de datos, tal como exige el Anexo 3.
# ============================================================

# Se importa datetime para marcar cada registro con fecha y hora.
from datetime import datetime
# Se importa os para crear la carpeta de logs si no existe.
import os


# Ruta de la carpeta donde se guardarán los archivos de log.
CARPETA_LOGS = "logs"
# Ruta completa del archivo de eventos.
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "eventos.log")


def _asegurar_carpeta() -> None:
    """Crea la carpeta de logs si todavía no existe.

    Se usa exist_ok=True para no lanzar error si ya está creada.
    """
    os.makedirs(CARPETA_LOGS, exist_ok=True)


def _escribir(nivel: str, mensaje: str) -> None:
    """Escribe una línea en el archivo de log.

    Parámetros:
        nivel   -> tipo de registro: INFO, ERROR, ADVERTENCIA.
        mensaje -> texto descriptivo de lo ocurrido.

    Se envuelve en try/except/finally porque escribir en disco
    también puede fallar (permisos, disco lleno) y el sistema
    nunca debe caerse por un problema de logging.
    """
    try:
        # Se garantiza que la carpeta exista antes de escribir.
        _asegurar_carpeta()
        # Se arma la marca de tiempo con formato legible.
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Se abre el archivo en modo 'a' (append) para no borrar
        # los registros anteriores, con codificación UTF-8.
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            # Se escribe la línea con nivel, fecha y mensaje.
            archivo.write(f"[{marca}] [{nivel}] {mensaje}\n")
    except OSError as error:
        # Si falla la escritura, se informa por consola pero el
        # programa continúa: el logging nunca debe romper la app.
        print(f"No se pudo escribir en el log: {error}")
    finally:
        # El bloque finally se ejecuta siempre, haya error o no.
        # Aquí no hay recursos que liberar porque 'with' ya cerró
        # el archivo, pero se deja explícito para cumplir la guía.
        pass


def registrar_info(mensaje: str) -> None:
    """Registra un evento normal del sistema."""
    _escribir("INFO", mensaje)


def registrar_error(mensaje: str) -> None:
    """Registra un error controlado del sistema."""
    _escribir("ERROR", mensaje)


def registrar_advertencia(mensaje: str) -> None:
    """Registra una situación anómala que no detiene el sistema."""
    _escribir("ADVERTENCIA", mensaje)