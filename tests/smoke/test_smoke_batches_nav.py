import pytest

from pages.menu.batches.menu_batches import MenuBatchesPage
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_rutas_navegacion_continua, ejecutar_logout_seguro


@pytest.mark.smoke
@pytest.mark.batches
def test_smoke_navegacion_menu_batches(auth,page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas (grupos) del menú Batches.
    """
    nombre_caso_prueba = "Smoke_Navegacion_Menu_Batches"
    logger_test = get_logger(nombre_caso_prueba)

    logger_test.info(f"INICIO: Ejecutando SMOKE TEST de Navegación del Menú Batches: '{nombre_caso_prueba}'")

    pagina_batches = MenuBatchesPage(page)

    logger_test.info("Paso 1: Iniciando flujo de autenticación (LOGIN).")
    try:
        auth.login_con_env(caso=nombre_caso_prueba)
        logger_test.info("Login exitoso.")
    except Exception as e:
        logger_test.critical(f"FALLO CRÍTICO: No se pudo realizar el login. Error: {e}", exc_info=True)
        pytest.fail(f"El test no puede continuar sin un login exitoso. Error: {e}")

    # Definición de las rutas de navegación con los métodos de MenuBatchesPage
    rutas_de_navegacion = [
        # PASO INICIAL: Entrar a la consola
        ("Batches > Consola de Batches",
         pagina_batches.navegar_a_consola_batches),

        ("Batches > Comercial Adquirente",
         pagina_batches.navegar_a_grupo_comercial_adquirente),

        ("Batches > Adquirente",
         pagina_batches.navegar_a_grupo_adquirente),

        ("Batches > Comercio Adquirente",
         pagina_batches.navegar_a_grupo_comercio_adquirente),

        ("Batches > Común",
         pagina_batches.navegar_a_grupo_comun),

        ("Batches > Reportes Adquirente",
         pagina_batches.navegar_a_grupo_reportes_adquirente),

        ("Batches > Transacción Adquirente",
         pagina_batches.navegar_a_grupo_transaccion_adquirente),
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
