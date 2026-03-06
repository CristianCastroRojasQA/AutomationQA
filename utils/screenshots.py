import os
import shutil
from datetime import datetime
from playwright.sync_api import Page
from utils.logger import get_logger

log = get_logger("Screenshot")

# Registro en memoria para asegurar que la limpieza ocurra solo una vez por ejecución
_carpetas_limpiadas = set()


def capturar_evidencia(page: Page, nombre_caso: str, nombre_paso: str) -> None:
    """
    Captura el contenido del navegador y gestiona el saneamiento de carpetas.
    Sustituye a pyautogui por el método nativo de Playwright.
    """
    global _carpetas_limpiadas

    base_folder = "screenshots"
    case_folder = os.path.join(base_folder, nombre_caso)

    # 1. Lógica de saneamiento: Borra los archivos internos, no la carpeta
    if nombre_caso not in _carpetas_limpiadas:
        if os.path.exists(case_folder):
            log.info(f"Limpiando evidencias anteriores en: {case_folder}")
            for archivo in os.listdir(case_folder):
                file_path = os.path.join(case_folder, archivo)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    log.error(f"No se pudo borrar {file_path}: {e}")

        # Asegura que la carpeta exista
        os.makedirs(case_folder, exist_ok=True)
        _carpetas_limpiadas.add(nombre_caso)

    # 2. Construcción de la ruta con marca de tiempo
    timestamp = datetime.now().strftime("%H-%M-%S")
    path = os.path.join(case_folder, f"{timestamp}_{nombre_paso}.png")

    # 3. Captura nativa de Playwright
    try:
        page.wait_for_timeout(500)
        # full_page=True capturaría todo el scroll, pero para pasos normales el viewport basta
        page.screenshot(path=path)
        log.info(f"Captura de navegador guardada en: {path}")
    except Exception as e:
        log.error(f"Error al capturar pantalla en {path}: {e}")
