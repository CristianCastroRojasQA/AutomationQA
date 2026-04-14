import re
from datetime import datetime
from playwright.sync_api import Page

from core.config.settings import settings
from core.utils.logger import get_logger

log = get_logger("Screenshot")


def capturar_evidencia(page: Page, nombre_caso: str, nombre_paso: str) -> None:
    """
    Captura una pantalla del estado actual del navegador y la persiste en disco.

    Organización de archivos:
        EVIDENCIAS_DIR / YYYY-MM-DD / nombre_caso / HH-MM-SS_nombre_paso.png

    Args:
        page: Instancia activa de Playwright Page.
        nombre_caso: Identificador del test (usado como nombre de carpeta).
        nombre_paso: Etiqueta del momento de captura (usado en el nombre del archivo).
    """
    try:
        log.debug(f"Iniciando captura de pantalla para el paso: '{nombre_paso}'...")

        # 1. Preparar carpeta con ruta dinámica desde settings
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        folder_caso = settings.EVIDENCIAS_DIR / fecha_hoy / nombre_caso
        folder_caso.mkdir(parents=True, exist_ok=True)

        log.debug(f"Directorio de evidencias verificado: {folder_caso}")

        # 2. Sanitizar nombre del archivo (elimina caracteres inválidos en Windows)
        timestamp = datetime.now().strftime("%H-%M-%S")
        nombre_paso_limpio = re.sub(r'[<>:"/\\|?*]', '_', nombre_paso)
        path_captura = folder_caso / f"{timestamp}_{nombre_paso_limpio}.png"

        # 3. Espera de estabilización de UI antes de capturar
        log.debug(f"Esperando {settings.ANIMATION_WAIT}ms para estabilización de UI...")
        page.wait_for_timeout(settings.ANIMATION_WAIT)

        # 4. Captura
        page.screenshot(path=path_captura, full_page=False)
        log.info(f"EVIDENCIA: {path_captura.name} generada exitosamente.")

    except Exception as e:
        log.error(
            f"ERROR DE INFRAESTRUCTURA: No se pudo guardar la captura en "
            f"{locals().get('path_captura', 'ruta no definida')}. "
            f"Motivo: {e}"
        )
