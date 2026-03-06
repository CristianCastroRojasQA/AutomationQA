import pytest
from flows.auth_flow import AuthFlow
from pages.menu.menu_configuracion import MenuConfiguracionPage
from utils.logger import get_logger

# Lista de navegaciones (con el fix de 'ValuesSearch' que detectamos)
NAVEGACIONES_CONFIGURACION = [
    ("marca_modelos_terminales", "ABCUC022"),
    ("terminales_alta_terminal", "ABCUC023"),
    ("terminales_mantenimiento_terminales", "ABCUC024"),
    ("terminales_alta_masiva_terminales", "ABCUC039"),
    ("terminales_consulta_stock_terminales", "Check-Terminal-Stock"),
    ("productos_alta_productos", "ABCUC025_AddProduct"),
    ("productos_mantenimiento_productos", "ABCUC025_ModifyProduct"),
    ("mantenimiento_calendario_adquirente", "ABCUC015"),
    ("mantenimiento_tasa_cambio", "ABCUC016"),
    ("mantenimiento_condiciones_comerciales", "AMUC016"),
    ("mantenimiento_condiciones_comerciales_promocionales", "AMRUC045"),
    ("reporte_condiciones_comerciales", "AMRUC047"),
    ("mantenimiento_grupo_economico", "ABCUC046"),
    ("mantenimiento_actividad_economica", "ABCUC047"),
    ("mantenimiento_parametros_calculo_mdr", "mdr-brand-parameters"),
    ("gestion_alta_lista_reglas_autorizacion", "AddAuthorizationRuleList"),
    ("gestion_mantenimiento_lista_reglas_autorizacion", "UpdateAuthorizationRuleListSearch"),
    ("gestion_mantenimiento_valores_lista_reglas_autorizacion", "UpdateAuthorizationRuleListValuesSearch"),
    ("gestion_eliminar_listas_reglas_autorizacion", "DeleteAuthorizationRuleList"),
]


@pytest.mark.smoke
@pytest.mark.configuracion
def test_TC_nav_menu_configuracion(page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas del menú Configuración.
    """
    caso = "Smoke_Nav_Configuracion"
    log = get_logger(caso)

    auth = AuthFlow(page)
    menu_cfg = MenuConfiguracionPage(page)

    log.info("--- INICIO SMOKE TEST: LOGIN ---")
    auth.login_con_env(caso=caso)

    errores = []

    for metodo, esperado in NAVEGACIONES_CONFIGURACION:
        log.info(f"Ejecutando: {metodo}")
        try:
            funcion = getattr(menu_cfg, metodo)
            url = funcion(caso)

            if esperado not in url:
                error_msg = f"[{metodo}] URL incorrecta. Esperaba: {esperado} | Obtuve: {url}"
                log.error(error_msg)
                errores.append(error_msg)
            else:
                log.info(f"[{metodo}] OK")

        except Exception as e:
            msg = f"Error crítico en {metodo}: {str(e)}"
            log.error(msg)
            errores.append(msg)

    log.info("--- FIN SMOKE TEST: LOGOUT ---")
    auth.logout(caso=caso)

    if errores:
        pytest.fail(f"Fallos en Smoke Test de Configuración:\n" + "\n".join(errores))
