import pytest

from pages.menu.batches.menu_batches import MenuBatchesPage
from utils.common_actions import realizar_login_obligatorio, finalizar_sesion_segura
from utils.logger import get_logger
from utils.test_orchestrator import TestOrchestrator


@pytest.mark.smoke
@pytest.mark.batches
def test_smoke_navegacion_menu_batches(auth, page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas (grupos) del menú Batches.
    """
    nombre_caso_prueba = "Smoke_Navegacion_Menu_Batches"
    logger = get_logger(nombre_caso_prueba)
    pagina_batches = MenuBatchesPage(page)

    realizar_login_obligatorio(auth, nombre_caso_prueba, logger)

    rutas_de_navegacion = [
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

    engine = TestOrchestrator(page, logger, nombre_caso_prueba)
    try:
        engine.ejecutar_flujo(rutas_de_navegacion)
    finally:
        finalizar_sesion_segura(auth, logger, nombre_caso_prueba)
