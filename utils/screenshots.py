from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page
from utils.logger import get_logger

log = get_logger("Screenshot")


def capturar_evidencia(page: Page, nombre_caso: str, nombre_paso: str) -> None:
    """
    Captura el contenido del navegador de forma nativa con Playwright
    organizando las evidencias por Fecha -> Caso -> Hora en la RAÍZ del proyecto.
    """
    try:
        # ---------------------------------------------------------
        # 1. GESTIÓN DE RUTAS CON PATHLIB
        # ---------------------------------------------------------

        # Resolvemos la raíz subiendo un nivel desde la carpeta 'utils'
        root_dir = Path(__file__).resolve().parent.parent
        screenshot_dir = root_dir / "screenshots"

        # MEJORA: Estructura jerárquica por fecha para no perder historial
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")

        # Ruta final:screenshots/YYYY-MM-DD/Nombre_Caso/
        folder_caso = screenshot_dir / fecha_hoy / nombre_caso

        # Aseguramos que toda la estructura de carpetas exista (mkdir con pathlib)
        folder_caso.mkdir(parents=True, exist_ok=True)

        # ---------------------------------------------------------
        # 2. CONSTRUCCIÓN DEL NOMBRE DEL ARCHIVO
        # ---------------------------------------------------------

        # Timestamp detallado (Hora-Minuto-Segundo)
        timestamp = datetime.now().strftime("%H-%M-%S")

        # Nombre del archivo: 14-30-05_Paso_X.png
        # Usamos el operador '/' de pathlib para unir la ruta y el nombre
        path_captura = folder_caso / f"{timestamp}_{nombre_paso}.png"

        # ---------------------------------------------------------
        # 3. CAPTURA NATIVA DE PLAYWRIGHT
        # ---------------------------------------------------------

        # Pequeña espera por seguridad para que la pantalla renderice
        page.wait_for_timeout(300)

        # Captura de pantalla nativa (Playwright se encarga de que la página cargue)
        # Nota: Playwright 1.12+ maneja los paths de pathlib sin problema.
        page.screenshot(path=path_captura)

        log.info(f"Captura de navegador guardada en: {path_captura}")

    except Exception as e:
        log.error(f"Error crítico al intentar capturar pantalla de evidence: {e}")
