import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # 1. Identificación del entorno
    PROYECTO = os.getenv("PROYECTO", "BPAGOS").upper()
    AMBIENTE = os.getenv("AMBIENTE", "CERT").upper()
    _prefix = f"{PROYECTO}_{AMBIENTE}"

    # 2. Datos de Aplicación (Web)
    URL = os.getenv(f"{_prefix}_URL")
    USUARIO = os.getenv(f"{_prefix}_USER")
    PASSWORD = os.getenv(f"{_prefix}_PASS")

    # 4. Validación de seguridad
    if not URL or not USUARIO or not PASSWORD:
        raise ValueError(
            f"❌ ERROR CRÍTICO: No se encontraron variables para {_prefix} en el .env. "
            f"Asegúrate de tener {_prefix}_URL, {_prefix}_USER y {_prefix}_PASS configurados."
        )

    # 3. Datos de Base de Datos
    DB_SERVER = os.getenv("SERVER_NAME")
    DB_USER = os.getenv("SESION_START")
    DB_PASS = os.getenv("PASSWORD")
    DB_NAME = os.getenv(f"{_prefix}_DB")

    if not DB_NAME or not DB_SERVER:
        raise ValueError(f"❌ ERROR: Configuración de DB no encontrada para {_prefix}")

    # 4. Configuración Técnica
    BROWSER = os.getenv("BROWSER", "chromium")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
    ANIMATION_WAIT = int(os.getenv("ANIMATION_WAIT", "500"))
    SCREENSHOT_ON_FAIL = os.getenv("SCREENSHOT_ON_FAIL", "true").lower() == "true"
    TRACE_ON_FAIL = os.getenv("TRACE_ON_FAIL", "true").lower() == "true"


settings = Settings()
