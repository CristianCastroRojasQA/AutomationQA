# utils/smoke_navigation_runner.py
from logging import Logger
from typing import Callable, List, Tuple

from playwright.sync_api import Page

from utils.screenshots import capturar_evidencia


def ejecutar_rutas_navegacion_continua(
        *,
        page: Page,
        nombre_caso_prueba: str,
        logger_test: Logger,
        rutas_de_navegacion: List[Tuple[str, Callable[[str], str]]],
) -> None:
    """
    Ejecuta rutas de navegación, continúa aunque falle una,
    y al final falla si hubo errores (con resumen).
    """
    lista_de_errores = []

    for nombre_ruta, funcion_navegacion in rutas_de_navegacion:
        logger_test.info(f"Paso de prueba: Intentando navegar a: {nombre_ruta}")
        try:
            funcion_navegacion(nombre_caso_prueba)
            logger_test.info(f"ÉXITO: Navegación a '{nombre_ruta}' completada correctamente.")

        except Exception as e:
            logger_test.error(
                f"FALLO: Error durante la navegación a '{nombre_ruta}'. Detalles: {e}",
                exc_info=True
            )
            lista_de_errores.append(f"- {nombre_ruta}: {repr(e)}")

            etiqueta_evidencia_fallo = (
                f"ERROR_{nombre_ruta}"
                .replace(" ", "_")
                .replace("&gt;", "")
                .replace(">", "")
                .replace("-", "_")
            )

            logger_test.warning(
                f"Capturando evidencia de fallo para '{nombre_ruta}' con etiqueta: '{etiqueta_evidencia_fallo}'."
            )
            capturar_evidencia(page, nombre_caso_prueba, etiqueta_evidencia_fallo)

    if lista_de_errores:
        resumen_errores = "\n".join(lista_de_errores)
        logger_test.error(
            f"FIN: SMOKE TEST terminó con {len(lista_de_errores)} fallos."
        )
        raise AssertionError(
            "SMOKE terminó con fallos en las siguientes rutas:\n"
            f"{resumen_errores}"
        )

    logger_test.info("FIN: SMOKE TEST completado exitosamente sin fallos.")


def ejecutar_logout_seguro(*, flujo_autenticacion, logger_test: Logger, nombre_caso_prueba: str) -> None:
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
