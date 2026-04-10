import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Cerebro central de configuración.
    Gestiona rutas, credenciales dinámicas y validaciones de seguridad.
    """

    # --- 1. GESTIÓN DE RUTAS REALES ---
    # ROOT_DIR se clava a la carpeta raíz del proyecto independientemente de este archivo
    ROOT_DIR = Path(__file__).resolve().parent.parent

    # Nombres de carpetas desde .env con valores por defecto (fallbacks)
    _folder_evidencias = os.getenv("FOLDER_EVIDENCIAS", "screenshots")
    _folder_logs = os.getenv("FOLDER_LOGS", "logs")

    EVIDENCIAS_DIR = ROOT_DIR / _folder_evidencias
    LOGS_DIR = ROOT_DIR / _folder_logs

    # --- 2. SELECTORES DE ENTORNO ---
    PROYECTO = os.getenv("PROYECTO", "BPAGOS").upper()
    AMBIENTE = os.getenv("AMBIENTE", "CERT").upper()
    PREFIX = f"{PROYECTO}_{AMBIENTE}"

    # --- 3. DATOS DE APLICACIÓN (DINÁMICOS) ---
    URL = os.getenv(f"{PREFIX}_URL")
    USUARIO = os.getenv(f"{PREFIX}_USER")
    PASSWORD = os.getenv(f"{PREFIX}_PASS")

    # --- 4. DATOS DE BASE DE DATOS ---
    DB_SERVER = os.getenv("SERVER_NAME")
    DB_USER = os.getenv("SESION_START")
    DB_PASS = os.getenv("PASSWORD")
    DB_NAME = os.getenv(f"{PREFIX}_DB")

    # --- 5. CONFIGURACIÓN TÉCNICA (NORMALIZADA) ---
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    BROWSER = os.getenv("BROWSER", "chromium").lower()
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
    ANIMATION_WAIT = int(os.getenv("ANIMATION_WAIT", "500"))

    # Normalización de booleanos para evitar errores de texto en el .env
    HEADLESS = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
    SCREENSHOT_ON_FAIL = os.getenv("SCREENSHOT_ON_FAIL", "true").lower() in ("true", "1", "yes")

    def __init__(self):
        """Inicializa y garantiza que el entorno sea seguro para el test."""
        self._preparar_entorno()
        self._ejecutar_auditoria_config()

    def _preparar_entorno(self):
        """Crea las carpetas necesarias si no existen."""
        self.EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    def _ejecutar_auditoria_config(self):
        """
        Valida todas las variables críticas.
        Si faltan varias, las reporta todas juntas en un solo error.
        """
        errores = []

        # Validación Web
        if not self.URL: errores.append(f"{self.PREFIX}_URL")
        if not self.USUARIO: errores.append(f"{self.PREFIX}_USER")
        if not self.PASSWORD: errores.append(f"{self.PREFIX}_PASS")

        # Validación DB
        if not self.DB_SERVER: errores.append("SERVER_NAME")
        if not self.DB_NAME: errores.append(f"{self.PREFIX}_DB")
        if not self.DB_USER: errores.append("SESION_START")

        if errores:
            mensaje = (
                f"\n[CONFIG ERROR] Se detectaron variables faltantes para el entorno {self.PREFIX}:\n"
                f"Variables a revisar en .env: {', '.join(errores)}\n"
            )
            # Usamos un print simple antes del error porque el logger podría no estar listo
            print(mensaje)
            raise ValueError(mensaje)


# Instancia global para ser importada: from config.settings import settings
settings = Settings()
