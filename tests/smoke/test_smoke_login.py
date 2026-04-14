import pytest
from pages.login_page import LoginPage
from utils.common_actions import finalizar_sesion_segura, realizar_login_obligatorio
from utils.logger import get_logger


@pytest.mark.smoke
@pytest.mark.login
def test_smoke_login_logout_basico(auth, page):
    nombre_caso = "Smoke_Login_Basico"
    logger = get_logger(nombre_caso)
    pagina_login = LoginPage(page)

    # Variable de control para saber si el logout ya se hizo
    logout_realizado = False

    try:
        logger.debug("Comprobando que la página de destino es el formulario de acceso.")
        pagina_login.validar_presencia_login()
        realizar_login_obligatorio(auth, nombre_caso, logger)

        logger.info("PASO: Ejecutando cierre de sesión funcional desde la UI.")

        # Logout funcional (el que queremos probar)
        auth.logout(caso=nombre_caso)
        logout_realizado = True  # Marcamos como completado

        pagina_login.validar_retorno_a_login()

        logger.info("FIN: Verificación de retorno a pantalla de acceso exitosa.")

    finally:
        # SOLO ejecutamos la limpieza técnica si el logout funcional NO se completó
        # Esto elimina el WARNING cuando el test sale bien
        if not logout_realizado:
            logger.warning(
                f"TEARDOWN: Ejecutando salida forzada para {nombre_caso}. "
                "El flujo no cerró sesión solo."
            )
            finalizar_sesion_segura(auth, logger, nombre_caso)
        else:
            logger.debug("TEARDOWN: Sesión previamente cerrada. Saltando limpieza preventiva.")
