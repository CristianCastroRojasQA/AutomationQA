import pytest

from pages.menu.operaciones.menu_operaciones import MenuOperacionesPage
from utils.common_actions import realizar_login_obligatorio, finalizar_sesion_segura
from utils.logger import get_logger
from utils.test_orchestrator import TestOrchestrator


@pytest.mark.smoke
@pytest.mark.operaciones
def test_smoke_navegacion_menu_operaciones(auth, page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas del menú Operaciones.
    """
    nombre_caso_prueba = "Smoke_Navegacion_Menu_Operaciones"
    logger = get_logger(nombre_caso_prueba)
    pagina_operaciones = MenuOperacionesPage(page)

    realizar_login_obligatorio(auth, nombre_caso_prueba, logger)

    rutas_de_navegacion = [

        ("Operaciones > Consultar Débitos Automáticos",
         pagina_operaciones.navegar_a_consultar_debitos_automaticos),

        ("Operaciones > Mantenimiento Fee Collection Adquirente",
         pagina_operaciones.navegar_a_mantenimiento_fee_collection),

        ("Operaciones > Mantenimiento Pagos",
         pagina_operaciones.navegar_a_mantenimiento_pagos),

        ("Operaciones > Devolución Manual",
         pagina_operaciones.navegar_a_devolucion_manual),

        ("Operaciones > Administración Disputas Adquirente",
         pagina_operaciones.navegar_a_administracion_disputas_adquirente),

        ("Operaciones > Devolución Débitos Automáticos",
         pagina_operaciones.navegar_a_devolucion_debitos_automaticos),

        ("Operaciones > Cuadratura",
         pagina_operaciones.navegar_a_cuadratura)
    ]


    engine = TestOrchestrator(page, logger, nombre_caso_prueba)
    try:
        engine.ejecutar_flujo(rutas_de_navegacion)
    finally:
        finalizar_sesion_segura(auth, logger, nombre_caso_prueba)
