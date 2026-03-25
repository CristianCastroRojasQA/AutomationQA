import pytest
from flows.auth_flow import AuthFlow
from pages.login_page import LoginPage
from utils.logger import get_logger


@pytest.mark.smoke
@pytest.mark.login
def test_TC_smoke_login_logout_basico(page):
    """
    SMOKE LOGIN TEST

    Objetivo:
    - Verificar que el formulario de login está disponible
    - Ejecutar login exitoso
    - Confirmar que la sesión queda activa
    - Ejecutar logout
    - Validar retorno a la pantalla de login
    """

    caso = "Smoke_Login"
    log = get_logger(caso)

    auth = AuthFlow(page)
    login_pg = LoginPage(page)

    # -------------------------------------------------
    # PASO 1: Validar disponibilidad del login
    # -------------------------------------------------
    log.info("PASO 1: Validar formulario de login")
    login_pg.validar_en_login()

    # -------------------------------------------------
    # PASO 2: Ejecutar login
    # -------------------------------------------------
    log.info("PASO 2: Ejecutar login")
    nombre_usuario = auth.login_con_env(caso=caso)

    # Validación mínima y crítica del smoke
    assert nombre_usuario, (
        "El login se ejecutó, pero no se detectó indicador de sesión activa"
    )

    # -------------------------------------------------
    # PASO 3: Ejecutar logout
    # -------------------------------------------------
    log.info("PASO 3: Ejecutar logout")
    auth.logout(caso=caso)

    # -------------------------------------------------
    # PASO 4: Validar retorno al login
    # -------------------------------------------------
    log.info("PASO 4: Validar retorno al login")
    login_pg.validar_retorno_login()

    log.info("SMOKE LOGIN COMPLETADO EXITOSAMENTE")
