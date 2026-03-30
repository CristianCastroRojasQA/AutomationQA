import pytest

from pages.menu.seguridad.log_auditoria_menu_page import LogAuditoriaPage
from pages.menu.seguridad.mantenimiento_funcionalidad_menu_page import MantenimientoFuncionalidadPage
from pages.menu.seguridad.perfiles_menu_page import PerfilesMenuPage
from pages.menu.seguridad.politicas_seguridad_menu_page import PoliticasSeguridadPage
from pages.menu.seguridad.reportes_menu_page import ReportesMenuPage
from pages.menu.seguridad.usuario_menu_page import UsuariosMenuPage
from pages.menu.seguridad.validacion_controles_menu_page import ValidacionControlesMenuPage
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_rutas_navegacion_continua, ejecutar_logout_seguro


@pytest.mark.smoke
@pytest.mark.seguridad
def test_smoke_navegacion_menu_seguridad(auth, page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas del menú Seguridad.
    """
    nombre_caso_prueba = "Smoke_Navegacion_Menu_Seguridad"
    logger_test = get_logger(nombre_caso_prueba)

    logger_test.info(f"INICIO: Ejecutando SMOKE TEST de Navegación del Menú Seguridad: '{nombre_caso_prueba}'")

    pagina_usuarios_menu = UsuariosMenuPage(page)
    pagina_perfiles_menu = PerfilesMenuPage(page)
    pagina_validacion_menu = ValidacionControlesMenuPage(page)
    pagina_reportes_menu = ReportesMenuPage(page)
    pagina_mantenimiento_funcionalidad_menu = MantenimientoFuncionalidadPage(page)
    pagina_politicas_menu = PoliticasSeguridadPage(page)
    pagina_log_menu = LogAuditoriaPage(page)

    logger_test.info("Paso 1: Iniciando flujo de autenticación (LOGIN).")
    try:
        auth.login_con_env(caso=nombre_caso_prueba)
        logger_test.info("Login exitoso.")
    except Exception as e:
        logger_test.critical(f"FALLO CRÍTICO: No se pudo realizar el login. Error: {e}", exc_info=True)
        pytest.fail(f"El test no puede continuar sin un login exitoso. Error: {e}")

    # Definición de las rutas de navegación con los nombres de métodos estandarizados
    rutas_de_navegacion = [

        ("Seguridad > Usuarios > Mantenimiento de Usuario",
         pagina_usuarios_menu.navegar_a_usuario_mantenimiento_usuarios),
        ("Seguridad > Usuarios > Alta de Usuario",
         pagina_usuarios_menu.navegar_a_usuario_alta_usuario),
        ("Seguridad > Usuarios > Habilitar Usuario Portal Comercio",
         pagina_usuarios_menu.navegar_a_usuario_habilitar_usuario_portal),
        ("Seguridad > Usuarios > Baja de Usuario",
         pagina_usuarios_menu.navegar_a_usuario_baja_usuario),

        ("Seguridad > Perfiles > Alta de Perfil",
         pagina_perfiles_menu.navegar_a_perfiles_alta_perfil),
        ("Seguridad > Perfiles > Mantenimiento de Perfil",
         pagina_perfiles_menu.navegar_a_perfiles_mantenimiento_perfil),
        ("Seguridad > Perfiles > Baja de Perfil",
         pagina_perfiles_menu.navegar_a_perfiles_baja_perfil),

        ("Seguridad > Validación de Controles > Mantenimiento de Niveles > Alta de Nivel",
         pagina_validacion_menu.navegar_a_validacion_controles_alta_perfil),
        ("Seguridad > Validación de Controles > Mantenimiento de Niveles > Mantenimiento de Nivel",
         pagina_validacion_menu.navegar_a_validacion_controles_mantenimiento_perfil),
        ("Seguridad > Validación de Controles > Mantenimiento de Niveles > Baja de Nivel",
         pagina_validacion_menu.navegar_a_validacion_controles_baja_perfil),

        ("Seguridad > Reportes > Reporte de Usuarios y Accesos",
         pagina_reportes_menu.navegar_a_reportes_usuarios_accesos),
        ("Seguridad > Reportes > Reporte de Perfiles",
         pagina_reportes_menu.navegar_a_reportes_perfiles),
        ("Seguridad > Reportes > Reporte de Intentos de Acceso",
         pagina_reportes_menu.navegar_a_reportes_intentos_acceso),

        ("Seguridad > Mantenimiento de Funcionalidad",
         pagina_mantenimiento_funcionalidad_menu.navegar_a_mantenimiento_funcionalidad),

        ("Seguridad > Configuración Políticas de Seguridad",
         pagina_politicas_menu.navegar_a_configuracion_politicas_seguridad),

        ("Seguridad > Log de Auditoría",
         pagina_log_menu.navegar_a_log_audtoria)
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
