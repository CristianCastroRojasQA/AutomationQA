import pytest

from pages.menu.comercios.menu_comercios import MenuComerciosPage
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_rutas_navegacion_continua, ejecutar_logout_seguro


@pytest.mark.smoke
@pytest.mark.comercios
def test_smoke_navegacion_menu_comercios(auth, page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas del menú Comercios.
    """
    nombre_caso_prueba = "Smoke_Navegacion_Menu_Comercios"
    logger_test = get_logger(nombre_caso_prueba)

    logger_test.info(f"INICIO: Ejecutando SMOKE TEST de Navegación del Menú Comercios: '{nombre_caso_prueba}'")

    pagina_comercios = MenuComerciosPage(page)

    logger_test.info("Paso 1: Iniciando flujo de autenticación (LOGIN).")
    try:
        auth.login_con_env(caso=nombre_caso_prueba)
        logger_test.info("Login exitoso.")
    except Exception as e:
        logger_test.critical(f"FALLO CRÍTICO: No se pudo realizar el login. Error: {e}", exc_info=True)
        pytest.fail(f"El test no puede continuar sin un login exitoso. Error: {e}")

    # Definición de las rutas de navegación con los nombres de métodos estandarizados

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
