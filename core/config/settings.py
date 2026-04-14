import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Cerebro central de configuración del framework.
    Gestiona rutas, credenciales dinámicas y configuración técnica.

    Responsabilidad: configuración GLOBAL del framework (browser, timeouts,
    rutas de artefactos, nivel de log). Las credenciales y URLs específicas
    de cada producto se cargan dinámicamente según PROYECTO + AMBIENTE del .env.

    Nota de arquitectura:
        Esta clase vive en core/ porque es compartida por todos los productos.
        Cada producto puede extender esta clase si necesita validaciones propias.
    """

    # --- 1. GESTIÓN DE RUTAS REALES ---
    # ROOT_DIR: raíz del proyecto (AutomationQA/), dos niveles arriba de core/config/
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent

    # Nombres de carpetas desde .env con valores por defecto (fallbacks)
    _folder_evidencias = os.getenv("FOLDER_EVIDENCIAS", "screenshots")
    _folder_logs = os.getenv("FOLDER_LOGS", "logs")

    EVIDENCIAS_DIR = ROOT_DIR / _folder_evidencias
    LOGS_DIR = ROOT_DIR / _folder_logs

    # --- 2. SELECTORES DE ENTORNO ---
    PROYECTO = os.getenv("PROYECTO", "BPAGOS").upper()
    AMBIENTE = os.getenv("AMBIENTE", "CERT").upper()
    PREFIX = f"{PROYECTO}_{AMBIENTE}"

    # --- 3. DATOS DE APLICACIÓN (DINÁMICOS POR PROYECTO + AMBIENTE) ---
    URL = os.getenv(f"{PREFIX}_URL")
    USUARIO = os.getenv(f"{PREFIX}_USER")
    PASSWORD = os.getenv(f"{PREFIX}_PASS")

    # --- 4. DATOS DE BASE DE DATOS ---
    DB_SERVER = os.getenv("SERVER_NAME")
    DB_USER = os.getenv("SESION_START")
    DB_PASS = os.getenv("PASSWORD")
    DB_NAME = os.getenv(f"{PREFIX}_DB")

    # --- 5. CONFIGURACIÓN TÉCNICA DEL FRAMEWORK (NORMALIZADA) ---
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    BROWSER = os.getenv("BROWSER", "chromium").lower()
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
    ANIMATION_WAIT = int(os.getenv("ANIMATION_WAIT", "500"))

    # Normalización de booleanos para evitar errores de texto en el .env
    HEADLESS = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
    SCREENSHOT_ON_FAIL = os.getenv("SCREENSHOT_ON_FAIL", "true").lower() in ("true", "1", "yes")

    def __init__(self):
        """Inicializa y garantiza que el entorno sea seguro para ejecutar tests."""
        self._preparar_entorno()
        from core.utils.logger import get_logger
        self.log = get_logger("Settings")
        self._ejecutar_auditoria_config()

        self.log.debug(
            f"Settings cargadas: Browser={self.BROWSER}, "
            f"Headless={self.HEADLESS}, Timeout={self.TIMEOUT}ms"
        )

    def _preparar_entorno(self):
        """Crea las carpetas de artefactos necesarias si no existen."""
        self.EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    def _ejecutar_auditoria_config(self):
        """
        Valida todas las variables críticas al inicio de la sesión.
        Si faltan varias, las reporta todas juntas en un solo error claro.
        """
        self.log.info(f"--- INICIO: Auditoría de Configuración para {self.PREFIX} ---")

        errores = []

        # Validación Web
        if not self.URL:      errores.append(f"{self.PREFIX}_URL")
        if not self.USUARIO:  errores.append(f"{self.PREFIX}_USER")
        if not self.PASSWORD: errores.append(f"{self.PREFIX}_PASS")

        # Validación DB
        if not self.DB_SERVER: errores.append("SERVER_NAME")
        if not self.DB_NAME:   errores.append(f"{self.PREFIX}_DB")
        if not self.DB_USER:   errores.append("SESION_START")

        if errores:
            mensaje = (
                f"\n[CONFIG ERROR] Variables faltantes para el entorno '{self.PREFIX}':\n"
                f"Revisa en .env: {', '.join(errores)}\n"
            )
            self.log.critical(mensaje)
            raise ValueError(mensaje)

        self.log.info(f"Configuración validada exitosamente para: {self.URL}")


# Instancia global — importar como: from core.config.settings import settings
settings = Settings()
