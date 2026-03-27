import logging
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler


class ColorFormatter(logging.Formatter):
    """Configura el formato visual con colores ANSI para la consola."""
    RESET = "\x1b[0m"
    BLUE = "\x1b[34;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    GREY = "\x1b[38;20m"
    CYAN_BOLD = "\x1b[36;1m"

    base_format = "%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s"

    FORMATS = {
        logging.DEBUG: GREY + base_format + RESET,
        logging.INFO: BLUE + base_format + RESET,
        logging.WARNING: YELLOW + base_format + RESET,
        logging.ERROR: RED + base_format + RESET,
        logging.CRITICAL: BOLD_RED + base_format + RESET,
    }

    def format(self, record):
        # Resaltado especial para hitos de ejecución
        if any(word in str(record.msg) for word in ["INICIO", "FIN", "PASO"]):
            log_fmt = self.CYAN_BOLD + self.base_format + self.RESET
        else:
            log_fmt = self.FORMATS.get(record.levelno, self.base_format)

        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


def get_logger(name="QA"):
    """
    Configura un logger profesional que detecta automáticamente la raíz
    del proyecto y organiza logs por fecha.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # --- GESTIÓN DE RUTAS CON PATHLIB ---
        # Resolvemos la raíz subiendo un nivel desde la carpeta 'utils'
        root_dir = Path(__file__).resolve().parent.parent
        log_dir = root_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Creamos un nombre de archivo dinámico por día (ej: ejecucion_2026-03-27.log)
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"ejecucion_{today}.log"

        # 1. Handler para CONSOLA (Con Colores)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter())
        logger.addHandler(console_handler)

        # 2. Handler para ARCHIVO (Rotativo y persistente)
        # 50MB por archivo, mantiene hasta 5 backups
        file_handler = RotatingFileHandler(
            log_file, maxBytes=50 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )

        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)-12s | %(filename)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
