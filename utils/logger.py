import logging
import os
from logging.handlers import TimedRotatingFileHandler


class ColorFormatter(logging.Formatter):
    """Configura el formato visual de los logs en consola utilizando códigos de color ANSI"""

    # Definición de códigos de colores para la terminal
    RESET = "\x1b[0m"
    BLUE = "\x1b[34;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    GREY = "\x1b[38;20m"
    CYAN_BOLD = "\x1b[36;1m"

    # Estructura base del mensaje de log
    base_format = "%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s"

    # Mapeo de niveles de log a sus respectivos colores
    FORMATS = {
        logging.DEBUG: GREY + base_format + RESET,
        logging.INFO: BLUE + base_format + RESET,
        logging.WARNING: YELLOW + base_format + RESET,
        logging.ERROR: RED + base_format + RESET,
        logging.CRITICAL: BOLD_RED + base_format + RESET,
    }

    def format(self, record):
        """Aplica un formato especial resaltado para los hitos de inicio y fin de caso"""
        if "INICIO" in str(record.msg) or "FIN" in str(record.msg):
            log_fmt = self.CYAN_BOLD + self.base_format + self.RESET
        else:
            log_fmt = self.FORMATS.get(record.levelno)

        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


def get_logger(name="QA"):
    """Inicializa y configura el sistema de logging dual: Consola y Archivo Rotativo"""
    logger = logging.getLogger(name)

    # Evita la duplicación de handlers si el logger ya fue instanciado
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # 1. Gestión de directorio de almacenamiento de evidencias textuales
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "ejecucion.log")

        # 2. Handler para salida por CONSOLA (Interfaz visual para el usuario)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter())
        logger.addHandler(console_handler)

        # 3. Handler para ARCHIVO DIARIO con política de retención de 7 días
        # midnight: Rota a las 00:00 | backupCount=7: Elimina archivos con antigüedad > 1 semana
        file_handler = TimedRotatingFileHandler(
            log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
        )

        # Formato técnico y detallado para persistencia en archivo (sin colores ANSI)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)-12s | %(filename)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
