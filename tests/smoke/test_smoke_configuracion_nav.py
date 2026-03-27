import pytest

from flows.auth_flow import AuthFlow
from pages.menu.configuracion.adquirente_menu_page import AdquirenteMenuPage
from pages.menu.configuracion.gestion_listas_menu_page import GestionListasMenuPage
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_rutas_navegacion_continua, ejecutar_logout_seguro


@pytest.mark.smoke
@pytest.mark.configuracion
def test_smoke_navegacion_menu_configuracion(auth,page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas del menú Configuración.
    """
    nombre_caso_prueba = "Smoke_Navegacion_Menu_Configuracion"
    logger_test = get_logger(nombre_caso_prueba)  # Obtiene el logger con el nombre del caso de prueba

    logger_test.info(f"INICIO: Ejecutando SMOKE TEST de Navegación del Menú Configuración: '{nombre_caso_prueba}'")

    pagina_adquirente_menu = AdquirenteMenuPage(page)
    pagina_gestion_listas_menu = GestionListasMenuPage(page)

    logger_test.info("Paso 1: Iniciando flujo de autenticación (LOGIN).")
    try:
        auth.login_con_env(caso=nombre_caso_prueba)
        logger_test.info("Login exitoso.")
    except Exception as e:
        logger_test.critical(f"FALLO CRÍTICO: No se pudo realizar el login. Error: {e}", exc_info=True)
        pytest.fail(f"El test no puede continuar sin un login exitoso. Error: {e}")

    # Definición de las rutas de navegación con los nombres de métodos estandarizados
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
