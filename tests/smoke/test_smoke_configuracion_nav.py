import pytest

from pages.menu.configuracion.adquirente_menu_page import AdquirenteMenuPage
from pages.menu.configuracion.gestion_listas_menu_page import GestionListasMenuPage
from utils.common_actions import realizar_login_obligatorio, finalizar_sesion_segura
from utils.logger import get_logger
from utils.test_orchestrator import TestOrchestrator


@pytest.mark.smoke
@pytest.mark.configuracion
def test_smoke_navegacion_menu_configuracion(auth, page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas del menú Configuración.
    """
    nombre_caso_prueba = "Smoke_Navegacion_Menu_Configuracion"
    logger = get_logger(nombre_caso_prueba)

    pagina_adquirente_menu = AdquirenteMenuPage(page)
    pagina_gestion_listas_menu = GestionListasMenuPage(page)

    realizar_login_obligatorio(auth, nombre_caso_prueba, logger)

    rutas_de_navegacion = [
        ("Configuración > Adquirente > Marcas y Modelos de Terminales",
         pagina_adquirente_menu.navegar_a_adquirente_marcas_y_modelos_terminales),

        ("Configuración > Adquirente > Terminales - Alta de Terminal",
         pagina_adquirente_menu.navegar_a_terminales_alta_terminal),
        ("Configuración > Adquirente > Terminales - Mantenimiento de Terminales",
         pagina_adquirente_menu.navegar_a_terminales_mantenimiento_terminales),
        ("Configuración > Adquirente > Terminales - Alta Masiva de Terminales",
         pagina_adquirente_menu.navegar_a_terminales_alta_masiva_terminales),
        ("Configuración > Adquirente > Terminales - Consulta Stock de Terminales",
         pagina_adquirente_menu.navegar_a_terminales_consulta_stock_terminales),

        ("Configuración > Adquirente > Productos - Alta de Producto",
         pagina_adquirente_menu.navegar_a_productos_alta_producto),
        ("Configuración > Adquirente > Productos - Mantenimiento de Producto",
         pagina_adquirente_menu.navegar_a_productos_mantenimiento_producto),

        ("Configuración > Adquirente > Mantenimiento Calendario Adquirente",
         pagina_adquirente_menu.navegar_a_adquirente_mantenimiento_calendario),
        ("Configuración > Adquirente > Mantenimiento Tasa de Cambio",
         pagina_adquirente_menu.navegar_a_adquirente_mantenimiento_tasa_cambio),

        ("Configuración > Adquirente > Condiciones Comerciales - Mantenimiento",
         pagina_adquirente_menu.navegar_a_condiciones_mantenimiento_condiciones_comerciales),
        ("Configuración > Adquirente > Condiciones Comerciales - Promocionales",
         pagina_adquirente_menu.navegar_a_condiciones_mantenimiento_condiciones_promocionales),
        ("Configuración > Adquirente > Condiciones Comerciales - Reporte",
         pagina_adquirente_menu.navegar_a_condiciones_reporte_condiciones_comerciales),

        ("Configuración > Adquirente > Mantenimiento Grupo Económico",
         pagina_adquirente_menu.navegar_a_adquirente_mantenimiento_grupo_economico),
        ("Configuración > Adquirente > Mantenimiento Actividad Económica",
         pagina_adquirente_menu.navegar_a_adquirente_mantenimiento_actividad_economica),
        ("Configuración > Adquirente > Mantenimiento Parámetros Cálculo MDR",
         pagina_adquirente_menu.navegar_a_adquirente_mantenimiento_parametros_calculo_mdr),

        ("Configuración > Gestión Listas > Alta Lista para Reglas de Autorizacion",
         pagina_gestion_listas_menu.navegar_a_gestion_alta_lista_reglas_autorizacion),
        ("Configuración > Gestión Listas > Mantenimiento de Lista para Reglas de Autorizacion",
         pagina_gestion_listas_menu.navegar_a_gestion_mantenimiento_lista_reglas_autorizacion),
        ("Configuración > Gestión Listas > Mantenimiento de Valores de Lista para Reglas de Autorización",
         pagina_gestion_listas_menu.navegar_a_gestion_mantenimiento_valores_lista_reglas_autorizacion),
        ("Configuración > Gestión Listas > Eliminar Lista para Reglas de autorización",
         pagina_gestion_listas_menu.navegar_a_gestion_eliminar_listas_reglas_autorizacion)
    ]

    logger.debug(f"Configuradas {len(rutas_de_navegacion)} rutas para verificación de disponibilidad.")

    engine = TestOrchestrator(page, logger, nombre_caso_prueba)
    try:
        logger.info("PASO: Orquestando navegación para el menú configuración...")
        engine.ejecutar_flujo(rutas_de_navegacion)
    finally:
        logger.debug("Iniciando bloque de limpieza (Teardown) post-ejecución.")
        finalizar_sesion_segura(auth, logger, nombre_caso_prueba)
