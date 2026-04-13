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
        log.debug(f"Iniciando captura de pantalla para el paso: '{nombre_paso}'...")

        # 1. Preparar ruta usando settings
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        folder_caso = settings.EVIDENCIAS_DIR / fecha_hoy / nombre_caso
        folder_caso.mkdir(parents=True, exist_ok=True)

        log.debug(f"Directorio de evidencias verificado: {folder_caso}")

        # 2. Sanitizar nombre del archivo
        timestamp = datetime.now().strftime("%H-%M-%S")
        nombre_paso_limpio = re.sub(r'[<>:"/\\|?*]', '_', nombre_paso)
        path_captura = folder_caso / f"{timestamp}_{nombre_paso_limpio}.png"

        # 3. ESPERA DINÁMICA (Aquí usamos el ajuste de Settings)
        # Evita que la captura salga con elementos moviéndose o en blanco
        log.debug(f"Esperando {settings.ANIMATION_WAIT}ms para estabilización de UI...")
        page.wait_for_timeout(settings.ANIMATION_WAIT)

        # 4. Tomar la captura
        page.screenshot(path=path_captura, full_page=False)
        log.info(f"EVIDENCIA: {path_captura.name} generada exitosamente.")

    except Exception as e:
        log.error(
            f"ERROR DE INFRAESTRUCTURA: No se pudo guardar la captura en "
            f"{locals().get('path_captura', 'ruta no definida')}. "
            f"Motivo: {e}"
        )
