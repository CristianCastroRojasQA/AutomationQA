import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables desde el archivo .env a variables de entorno


class Settings:
    PROYECTO = os.getenv("PROYECTO", "GETNET")  # Nombre del proyecto para reportes
    AMBIENTE = os.getenv("AMBIENTE")  # Define si es QA, CERT o PROD
    URL = os.getenv("URL")  # URL base del aplicativo

    # Validación crítica: Si no hay ambiente o URL, el framework se detiene inmediatamente
    if not AMBIENTE:
        raise ValueError("Falta AMBIENTE en .env (ej: CERT, QA).")
    if not URL:
        raise ValueError("Falta URL en .env.")

    # Construcción dinámica de credenciales basada en el ambiente seleccionado
    USUARIO = os.getenv(f"USER_{AMBIENTE}")
    PASSWORD = os.getenv(f"PASSWORD_{AMBIENTE}")

    if not USUARIO or not PASSWORD:
        raise ValueError(f"Faltan credenciales para AMBIENTE={AMBIENTE}.")

    # Configuración de ejecución del navegador
    BROWSER = os.getenv("BROWSER", "chromium")  # Navegador por defecto
    HEADLESS = (
        os.getenv("HEADLESS", "false").lower() == "true"
    )  # True para ejecución en segundo plano
    TIMEOUT = int(
        os.getenv("TIMEOUT", "30000")
    )  # Tiempo máximo de espera en milisegundos

    # Flags para captura de evidencias en caso de error
    SCREENSHOT_ON_FAIL = os.getenv("SCREENSHOT_ON_FAIL", "true").lower() == "true"
    TRACE_ON_FAIL = os.getenv("TRACE_ON_FAIL", "true").lower() == "true"


settings = Settings()  # Instancia única para ser importada en todo el proyecto
