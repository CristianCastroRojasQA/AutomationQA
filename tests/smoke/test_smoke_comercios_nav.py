import pytest

from pages.menu.comercios.menu_comercios import MenuComerciosPage
from utils.common_actions import realizar_login_obligatorio, finalizar_sesion_segura
from utils.logger import get_logger
from utils.test_orchestrator import TestOrchestrator


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

    # Orquestación
    engine = TestOrchestrator(page, logger, nombre_caso_prueba)
    try:
        engine.ejecutar_flujo(rutas_de_navegacion)
    finally:
        # Post-condición
        finalizar_sesion_segura(auth, logger, nombre_caso_prueba)
