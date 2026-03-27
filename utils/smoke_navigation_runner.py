import re
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
            # Ejecución del paso
            funcion_navegacion(nombre_caso_prueba)
            logger_test.info(f"ÉXITO: Navegación a '{nombre_ruta}' completada correctamente.")

        except Exception as e:
            # 1. Registrar el error
            lista_de_errores.append(f"- {nombre_ruta}: {repr(e)}")
            logger_test.error(f"FALLO: Error en '{nombre_ruta}'. Detalles: {e}")

            # 2. Captura de evidencia (Corregido escape de '.')
            nombre_limpio = re.sub(r'[^\w\-_. ]', '_', nombre_ruta).replace(" ", "_")
            etiqueta_fallo = f"ERROR_{nombre_limpio}"
            capturar_evidencia(page, nombre_caso_prueba, etiqueta_fallo)

            # 3. RECUPERACIÓN: Si falla, intentamos recargar
            logger_test.warning(
                f"Intentando recargar página para limpiar estado tras fallo en '{nombre_ruta}'..."
            )
            page.reload()
            page.wait_for_load_state("networkidle")

    # --- CIERRE DEL TEST (Fuera del loop) ---

    if lista_de_errores:
        resumen_errores = "\n".join(lista_de_errores)
        logger_test.error(
            f"FIN: SMOKE TEST terminó con {len(lista_de_errores)} fallos."
        )
        # El raise solo ocurre si la lista tiene algo
        raise AssertionError(
            "SMOKE terminó con fallos en las siguientes rutas:\n"
            f"{resumen_errores}"
        )

    # Si llega aquí, es porque lista_de_errores estaba vacía
    logger_test.info("FIN: SMOKE TEST completado exitosamente sin fallos.")


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