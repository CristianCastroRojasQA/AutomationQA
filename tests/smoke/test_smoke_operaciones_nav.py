import pytest

from pages.menu.operaciones.menu_operaciones import MenuOperacionesPage
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_rutas_navegacion_continua, ejecutar_logout_seguro


@pytest.mark.smoke
@pytest.mark.operaciones
def test_smoke_navegacion_menu_operaciones(auth, page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas del menú Operaciones.
    """
    nombre_caso_prueba = "Smoke_Navegacion_Menu_Operaciones"
    logger_test = get_logger(nombre_caso_prueba)
    pagina_operaciones = MenuOperacionesPage(page)

    logger_test.info("Paso 1: Iniciando flujo de autenticación (LOGIN).")
    try:
        auth.login_con_env(caso=nombre_caso_prueba)
        logger_test.info("Login exitoso.")
    except Exception as e:
        logger_test.critical(f"FALLO CRÍTICO: No se pudo realizar el login. Error: {e}", exc_info=True)
        pytest.fail(f"El test no puede continuar sin un login exitoso. Error: {e}")

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

    try:
        ejecutar_rutas_navegacion_continua(
            page=page,
            nombre_caso_prueba=nombre_caso_prueba,
            logger_test=logger_test,
            rutas_de_navegacion=rutas_de_navegacion,
        )
    finally:
        ejecutar_logout_seguro(
            flujo_autenticacion=auth,
            logger_test=logger_test,
            nombre_caso_prueba=nombre_caso_prueba,
        )
