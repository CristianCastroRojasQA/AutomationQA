import pytest

from products.paystudio.pages.menu.comercios.menu_comercios import MenuComerciosPage
from products.paystudio.pages.common.error_handler_page import ErrorHandlerPage
from core.utils.common_actions import realizar_login_obligatorio, finalizar_sesion_segura
from core.utils.logger import get_logger
from core.utils.test_orchestrator import TestOrchestrator


@pytest.mark.smoke
@pytest.mark.comercios
def test_smoke_navegacion_menu_comercios(auth, page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas del menú Comercios.
    """
    nombre_caso_prueba = "Smoke_Navegacion_Menu_Comercios"
    logger = get_logger(nombre_caso_prueba)
    pagina_comercios = MenuComerciosPage(page)

    realizar_login_obligatorio(auth, nombre_caso_prueba, logger)

    rutas_de_navegacion = [
        ("Comercios > Consultar Comercio / Sucursal",
         pagina_comercios.navegar_a_consultar_comercio_sucursal),

        ("Comercios > Alta de Comercio",
         pagina_comercios.navegar_a_alta_comercio),

        ("Comercios > Mantenimiento Preafiliación Comercio",
         pagina_comercios.navegar_a_mantenimiento_preafilicion_comercio),

        ("Comercios > Alta Preafiliación Comercio",
         pagina_comercios.navegar_a_alta_preafilicion_comercio),

        ("Comercios > Consulta de Transacciones",
         pagina_comercios.navegar_a_consulta_transacciones)
    ]
    logger.debug(f"Configuradas {len(rutas_de_navegacion)} rutas para verificación de disponibilidad.")

    # Orquestación
    engine = TestOrchestrator(
        page, logger, nombre_caso_prueba,
        error_handler_factory=lambda pg: ErrorHandlerPage(pg),
    )
    try:
        logger.info("PASO: Orquestando navegación para el menú comercios...")
        engine.ejecutar_flujo(rutas_de_navegacion)
    finally:
        logger.debug("Iniciando bloque de limpieza (Teardown) post-ejecución.")
        finalizar_sesion_segura(auth, logger, nombre_caso_prueba)
