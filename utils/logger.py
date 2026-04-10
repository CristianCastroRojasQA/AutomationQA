import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from config.settings import settings


class ColorFormatter(logging.Formatter):
    """
    Formateador de logs que aplica colores ANSI según el nivel de severidad.
    Optimiza el rendimiento pre-creando instancias de formateadores para cada nivel.
    """
    RESET = "\x1b[0m"
    COLORS = {
        logging.DEBUG: "\x1b[38;20m",  # Gris: Información técnica detallada
        logging.INFO: "\x1b[34;20m",  # Azul: Flujo normal de ejecución
        logging.WARNING: "\x1b[33;20m",  # Amarillo: Advertencias
        logging.ERROR: "\x1b[31;20m",  # Rojo: Errores controlados
        logging.CRITICAL: "\x1b[31;1m",  # Rojo Negrita: Errores fatales
    }
    CYAN_BOLD = "\x1b[36;1m"  # Color para hitos del test (INICIO/FIN/PASO)

    base_format = "%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s"

    def __init__(self):
        super().__init__(datefmt="%H:%M:%S")
        # Diccionario de formateadores pre-construidos para evitar instanciación repetitiva
        self.formatters = {
            level: logging.Formatter(color + self.base_format + self.RESET, datefmt="%H:%M:%S")
            for level, color in self.COLORS.items()
        }
        # Formateador especial para resaltar los pasos lógicos del test
        self.hitos_formatter = logging.Formatter(self.CYAN_BOLD + self.base_format + self.RESET, datefmt="%H:%M:%S")

    def format(self, record):
        """
        Determina qué estilo aplicar al mensaje de log.
        Si el mensaje contiene palabras clave de flujo, aplica resaltado Cyan.
        """
        msg = str(record.msg)
        if any(word in msg for word in ["INICIO", "FIN", "PASO"]):
            return self.hitos_formatter.format(record)

        formatter = self.formatters.get(record.levelno)
        if not formatter:
            return logging.Formatter(self.base_format).format(record)
        return formatter.format(record)


def get_logger(name="QA"):
    """
    Constructor del Logger siguiendo el patrón Singleton (evita duplicidad de handlers).

    Configuraciones aplicadas:
    1. Nivel de Log: Dinámico desde .env (settings.LOG_LEVEL).
    2. Handler Consola: Salida con colores vía sys.stdout.
    3. Handler Archivo: Persistencia rotativa en la ruta definida por settings.LOGS_DIR.
    """
    logger = logging.getLogger(name)

    # Solo configuramos el logger si no tiene handlers previos (evita logs duplicados)
    if not logger.handlers:
        # 1. Definición del nivel de severidad (DEBUG, INFO, etc.)
        logger.setLevel(getattr(logging, settings.LOG_LEVEL))
        logger.propagate = False  # No propaga a logs raíz para mantener limpieza en consola

        # 2. Definición del nombre y ruta del archivo de log
        # settings.LOGS_DIR garantiza que se use la carpeta configurada en el .env
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = settings.LOGS_DIR / f"ejecucion_{today}.log"

        # 3. HANDLER PARA CONSOLA: Prioriza la visibilidad con ColorFormatter
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColorFormatter())
        logger.addHandler(console_handler)

        # 4. HANDLER PARA ARCHIVO: Prioriza el detalle técnico y la rotación de espacio
        # Mantiene hasta 5 archivos de 10MB cada uno
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        # Formato detallado para archivo (incluye archivo y línea de código)
        file_format = "%(asctime)s | %(levelname)-8s | %(name)-12s | %(filename)s:%(lineno)d | %(message)s"
        file_handler.setFormatter(logging.Formatter(file_format, datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(file_handler)

    return logger
