import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROYECTO = os.getenv("PROYECTO", "GETNET")
    AMBIENTE = os.getenv("AMBIENTE")
    URL = os.getenv("URL")

    if not AMBIENTE:
        raise ValueError("Falta AMBIENTE en .env (ej: CERT, QA).")
    if not URL:
        raise ValueError("Falta URL en .env.")

    USUARIO = os.getenv(f"USER_{AMBIENTE}")
    PASSWORD = os.getenv(f"PASSWORD_{AMBIENTE}")

    if not USUARIO or not PASSWORD:
        raise ValueError(
            f"Faltan credenciales para AMBIENTE={AMBIENTE}. "
            f"Se esperan USER_{AMBIENTE} y PASSWORD_{AMBIENTE}."
        )

    BROWSER = os.getenv("BROWSER", "chromium")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))

    SCREENSHOT_ON_FAIL = os.getenv("SCREENSHOT_ON_FAIL", "true").lower() == "true"
    TRACE_ON_FAIL = os.getenv("TRACE_ON_FAIL", "true").lower() == "true"


settings = Settings()
