import pytest

from pages.menu.seguridad.log_auditoria_menu_page import LogAuditoriaPage
from pages.menu.seguridad.mantenimiento_funcionalidad_menu_page import MantenimientoFuncionalidadPage
from pages.menu.seguridad.perfiles_menu_page import PerfilesMenuPage
from pages.menu.seguridad.politicas_seguridad_menu_page import PoliticasSeguridadPage
from pages.menu.seguridad.reportes_menu_page import ReportesMenuPage
from pages.menu.seguridad.usuario_menu_page import UsuariosMenuPage
from pages.menu.seguridad.validacion_controles_menu_page import ValidacionControlesMenuPage
from utils.common_actions import realizar_login_obligatorio, finalizar_sesion_segura
from utils.logger import get_logger
from utils.test_orchestrator import TestOrchestrator


@pytest.mark.smoke
@pytest.mark.seguridad
def test_smoke_navegacion_menu_seguridad(auth, page):
    """
    SMOKE TEST: Verifica la disponibilidad de todas las pantallas del menú Seguridad.
    """
    nombre_caso_prueba = "Smoke_Navegacion_Menu_Seguridad"
    logger = get_logger(nombre_caso_prueba)

    pagina_usuarios_menu = UsuariosMenuPage(page)
    pagina_perfiles_menu = PerfilesMenuPage(page)
    pagina_validacion_menu = ValidacionControlesMenuPage(page)
    pagina_reportes_menu = ReportesMenuPage(page)
    pagina_mantenimiento_funcionalidad_menu = MantenimientoFuncionalidadPage(page)
    pagina_politicas_menu = PoliticasSeguridadPage(page)
    pagina_log_menu = LogAuditoriaPage(page)

    realizar_login_obligatorio(auth, nombre_caso_prueba, logger)

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

    engine = TestOrchestrator(page, logger, nombre_caso_prueba)
    try:
        engine.ejecutar_flujo(rutas_de_navegacion)
    finally:
        finalizar_sesion_segura(auth, logger, nombre_caso_prueba)
