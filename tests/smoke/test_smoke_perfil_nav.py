import pytest

from pages.common.perfil_page import PerfilPage
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_rutas_navegacion_continua, ejecutar_logout_seguro


@pytest.mark.smoke
@pytest.mark.perfil
def test_smoke_opciones_perfil(auth, page):
    nombre_caso_prueba = "Smoke_Opciones_Perfil"
    logger_test = get_logger(nombre_caso_prueba)

    perfil = PerfilPage(page)

    # 1. Login Obligatorio
    try:
        auth.login_con_env(caso=nombre_caso_prueba)
        logger_test.info("Login exitoso.")
    except Exception as e:
        logger_test.critical(f"FALLO CRÍTICO: No se pudo realizar el login. Error: {e}", exc_info=True)
        pytest.fail(f"El test no puede continuar sin un login exitoso. Error: {e}")

    # 2. Definición de rutas
    rutas_perfil = [
        ("Perfil > Fecha de Negocio", perfil.validar_fecha_negocio_modal),
        ("Perfil > Cambiar Contraseña", perfil.navegar_a_cambiar_contrasena),
        ("Perfil > Acerca de", perfil.validar_version_ambiente)
    ]

    try:
        ejecutar_rutas_navegacion_continua(
            page=page,
            nombre_caso_prueba=nombre_caso_prueba,
            logger_test=logger_test,
            rutas_de_navegacion=rutas_perfil,
        )
    finally:
        ejecutar_logout_seguro(
            flujo_autenticacion=auth,
            logger_test=logger_test,
            nombre_caso_prueba=nombre_caso_prueba,
        )
