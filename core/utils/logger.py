import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler


class ColorFormatter(logging.Formatter):
    """
    Formateador de logs que aplica colores ANSI según el nivel de severidad.
    Optimiza el rendimiento pre-creando instancias de formateadores para cada nivel.
    """
    RESET = "\x1b[0m"
    COLORS = {
        logging.DEBUG:    "\x1b[38;20m",  # Gris:        Información técnica detallada
        logging.INFO:     "\x1b[34;20m",  # Azul:        Flujo normal de ejecución
        logging.WARNING:  "\x1b[33;20m",  # Amarillo:    Advertencias no críticas
        logging.ERROR:    "\x1b[31;20m",  # Rojo:        Errores controlados
        logging.CRITICAL: "\x1b[31;1m",   # Rojo Negrita: Errores fatales
    }
    CYAN_BOLD = "\x1b[36;1m"  # Color para hitos del test (INICIO / FIN / PASO)

    base_format = "%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s"

    def __init__(self):
        super().__init__(datefmt="%H:%M:%S")
        # Diccionario de formateadores pre-construidos por nivel (evita instanciación por cada log)
        self.formatters = {
            level: logging.Formatter(color + self.base_format + self.RESET, datefmt="%H:%M:%S")
            for level, color in self.COLORS.items()
        }
        # Formateador especial para resaltar hitos lógicos del test
        self.hitos_formatter = logging.Formatter(
            self.CYAN_BOLD + self.base_format + self.RESET, datefmt="%H:%M:%S"
        )

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


def get_logger(name: str = "QA") -> logging.Logger:
    """
    Constructor del Logger siguiendo el patrón Singleton por nombre.
    Evita duplicidad de handlers si el mismo logger es instanciado múltiples veces.

    Configuraciones:
        1. Nivel de log: dinámico desde .env (LOG_LEVEL).
        2. Handler consola: salida con colores ANSI vía sys.stdout.
        3. Handler archivo: rotativo en LOGS_DIR (máx 10MB × 5 archivos).

    Args:
        name: Identificador del logger (aparece en la columna 'name' del log).

    Returns:
        logging.Logger: Instancia configurada y lista para usar.
    """
    from core.config.settings import Settings

    logger = logging.getLogger(name)

    # Solo configuramos si no tiene handlers previos (patrón Singleton)
    if not logger.handlers:
        logger.setLevel(getattr(logging, Settings.LOG_LEVEL))
        logger.propagate = False  # Evita propagación al root logger (logs duplicados)

        # Ruta del archivo de log (un archivo por día)
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = Settings.LOGS_DIR / f"ejecucion_{today}.log"

        # Handler Consola: colores ANSI para visibilidad en terminal
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColorFormatter())
        logger.addHandler(console_handler)

        # Handler Archivo: detalle técnico con rotación automática
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB por archivo
            backupCount=5,               # Máximo 5 archivos históricos
            encoding="utf-8"
        )
        file_format = "%(asctime)s | %(levelname)-8s | %(name)-12s | %(filename)s:%(lineno)d | %(message)s"
        file_handler.setFormatter(logging.Formatter(file_format, datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(file_handler)

    return logger
