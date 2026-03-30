from datetime import datetime
from logging import Logger
from pathlib import Path

from pages.common.error_handler_page import ErrorHandlerPage
from utils.screenshots import capturar_evidencia


def ejecutar_rutas_navegacion_continua(
        page, nombre_caso_prueba, logger_test, rutas_de_navegacion
):
    lista_de_errores = []

    for nombre_ruta, funcion_navegacion in rutas_de_navegacion:
        logger_test.info(f"--- PASO: Intentando navegar a {nombre_ruta} ---")

        try:
            # 1. EJECUCIÓN NORMAL (Igual que antes)
            funcion_navegacion(nombre_caso_prueba)
            logger_test.info(f"ÉXITO: Pantalla '{nombre_ruta}' cargada correctamente.")

        except Exception as e:
            # 2. SE PRODUJO UN FALLO: ENTRA LA LOGICA DE DISCRIMINACIÓN
            handler = ErrorHandlerPage(page)

            if handler.hay_error():
                # --- ESCENARIO A: PANTALLA DE ERROR DE PAYSTUDIO ---
                logger_test.error(f"🚨 DETECTADA PANTALLA DE ERROR EN: {nombre_ruta}")

                # Extraemos el detalle técnico (Stack Trace)
                detalle = handler.obtener_detalle()

                # Evidencias (Foto + TXT)
                timestamp = datetime.now().strftime("%H-%M-%S")
                capturar_evidencia(page, nombre_caso_prueba, f"ERROR_FUNCIONAL_{nombre_ruta}")
                _guardar_detalle_error_txt(nombre_caso_prueba, nombre_ruta, detalle, timestamp)

                # Acción de recuperación: Clic en 'Aceptar' para intentar seguir
                handler.aceptar_y_recuperar()

                lista_de_errores.append(f"{nombre_ruta}: Error de Aplicación (Capturado detalle técnico)")

            else:
                # --- ESCENARIO B: ERROR TRADICIONAL (TIMEOUT, SELECTOR, ETC) ---
                # Mantenemos la funcionalidad que ya tenías antes
                msg_error = f"FALLO TÉCNICO en {nombre_ruta}: {str(e)[:100]}"
                logger_test.error(msg_error)

                # Captura estándar de fallo
                capturar_evidencia(page, nombre_caso_prueba, f"FALLO_TECH_{nombre_ruta}")

                # Tu lógica previa de recuperación: Reload
                logger_test.warning("Recargando página para intentar limpiar estado...")
                page.reload()
                page.wait_for_load_state("networkidle")

                lista_de_errores.append(f"{nombre_ruta}: Fallo de Automatización/Timeout")

    # Al finalizar reportamos los errores caidos
    if lista_de_errores:
        import pytest
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
