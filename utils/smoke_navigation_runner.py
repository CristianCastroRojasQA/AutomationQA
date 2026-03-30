from datetime import datetime
from logging import Logger
from pathlib import Path

import pytest

from pages.common.error_handler_page import ErrorHandlerPage
from utils.screenshots import capturar_evidencia


def ejecutar_rutas_navegacion_continua(
        page, nombre_caso_prueba, logger_test, rutas_de_navegacion
):
    lista_de_errores = []
    rutas_omitidas = []

    for nombre_ruta, funcion_navegacion in rutas_de_navegacion:
        logger_test.info(f"--- PASO: Intentando navegar a {nombre_ruta} ---")

        try:
            # 1. EJECUCIÓN NORMAL
            funcion_navegacion(nombre_caso_prueba)
            logger_test.info(f"ÉXITO: Pantalla '{nombre_ruta}' cargada correctamente.")

        except Exception as e:
            error_msg = str(e)

            # --- NUEVA LÓGICA: DETECCIÓN DE ENLACE NO DISPONIBLE ---
            # Si el error indica que el elemento no existe o no se pudo hacer clic por visibilidad "waiting for", "not visible", "not found", "Timeout"
            if any(key in error_msg for key in ["not found"]):
                logger_test.warning(
                    f"OMISIÓN: El enlace '{nombre_ruta}' no está disponible en este ambiente. Saltando...")
                rutas_omitidas.append(nombre_ruta)
                continue

            # --- ESCENARIO A: PANTALLA DE ERROR DE PAYSTUDIO ---
            handler = ErrorHandlerPage(page)
            if handler.hay_error():
                logger_test.error(f"DETECTADA PANTALLA DE ERROR EN: {nombre_ruta}")
                detalle = handler.obtener_detalle()

                timestamp = datetime.now().strftime("%H-%M-%S")
                capturar_evidencia(page, nombre_caso_prueba, f"ERROR_FUNCIONAL_{nombre_ruta}")
                _guardar_detalle_error_txt(nombre_caso_prueba, nombre_ruta, detalle, timestamp)

                handler.aceptar_y_recuperar()
                lista_de_errores.append(f"{nombre_ruta}: Error de Aplicación")

            else:
                # --- ESCENARIO B: FALLO TÉCNICO REAL (Otro tipo de error) ---
                logger_test.error(f"FALLO TÉCNICO en {nombre_ruta}: {error_msg[:100]}")
                capturar_evidencia(page, nombre_caso_prueba, f"FALLO_TECH_{nombre_ruta}")

                logger_test.warning("Recargando página para intentar limpiar estado...")
                page.reload()
                page.wait_for_load_state("networkidle")
                lista_de_errores.append(f"{nombre_ruta}: Fallo de Automatización")

    # --- RESUMEN FINAL ---
    if rutas_omitidas:
        logger_test.info(
            f"RESUMEN: Se omitieron {len(rutas_omitidas)} rutas por no estar disponibles: {rutas_omitidas}")

    if lista_de_errores:
        pytest.fail(f"El Smoke Test finalizó con {len(lista_de_errores)} errores:\n" + "\n".join(lista_de_errores))


def _guardar_detalle_error_txt(nombre_caso, ruta, detalle, ts):
    """Guarda el detalle técnico en la misma carpeta de screenshots."""
    root = Path(__file__).resolve().parent.parent
    fecha = datetime.now().strftime("%Y-%m-%d")
    folder = root / "screenshots" / fecha / nombre_caso
    folder.mkdir(parents=True, exist_ok=True)

    archivo = folder / f"{ts}_DETALLE_TECNICO.txt"
    archivo.write_text(f"RUTA: {ruta}\nHORA: {ts}\n\nDETALLE:\n{detalle}", encoding="utf-8")


def ejecutar_logout_seguro(
        *,
        flujo_autenticacion,
        logger_test: Logger,
        nombre_caso_prueba: str
) -> None:
    """
    Logout que no rompe el test si falla, pero deja trazabilidad.
    """
    logger_test.info("Paso final: Iniciando flujo de desautenticación (LOGOUT).")
    try:
        flujo_autenticacion.logout(caso=nombre_caso_prueba)
        logger_test.info("Logout exitoso.")
    except Exception as e:
        logger_test.warning(
            f"Advertencia: No se pudo realizar el logout correctamente. Error: {e}",
            exc_info=True
        )
