import re
from datetime import datetime
from playwright.sync_api import Page
from config.settings import settings
from utils.logger import get_logger

log = get_logger("Screenshot")


def capturar_evidencia(page: Page, nombre_caso: str, nombre_paso: str) -> None:
    """
    Captura pantalla esperando el tiempo configurado en el .env para asegurar
    que las animaciones de la interfaz hayan finalizado.
    """
    try:
        # 1. Preparar ruta usando settings
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        folder_caso = settings.EVIDENCIAS_DIR / fecha_hoy / nombre_caso
        folder_caso.mkdir(parents=True, exist_ok=True)

        # 2. Sanitizar nombre del archivo
        timestamp = datetime.now().strftime("%H-%M-%S")
        nombre_paso_limpio = re.sub(r'[<>:"/\\|?*]', '_', nombre_paso)
        path_captura = folder_caso / f"{timestamp}_{nombre_paso_limpio}.png"

        # 3. ESPERA DINÁMICA (Aquí usamos el ajuste de Settings)
        # Evita que la captura salga con elementos moviéndose o en blanco
        page.wait_for_timeout(settings.ANIMATION_WAIT)

        # 4. Tomar la captura
        page.screenshot(path=path_captura, full_page=False)

        log.info(f"Screenshot guardado: {path_captura.name}")

    except Exception as e:
        log.error(f"Error al capturar pantalla: {e}")
