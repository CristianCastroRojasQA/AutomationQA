from logging import Logger
import pytest

def realizar_login_obligatorio(auth, nombre_test: str, logger: Logger):
    """Ejecuta el login y detiene todo si falla (Pre-condición crítica)."""
    try:
        auth.login_con_env(caso=nombre_test)
        logger.info("Login exitoso.")
    except Exception as e:
        logger.critical(f"ERROR CRÍTICO AL INICIAR SESIÓN: {e}")
        pytest.fail("Abortando ejecución: Login fallido.")


def finalizar_sesion_segura(auth, logger: Logger, nombre_test: str):
    """Cierra la sesión garantizando que el test no falle por el logout."""
    logger.info(f"Finalizando sesión para el caso: {nombre_test}")
    try:
        auth.logout(caso=nombre_test)
    except Exception as e:
        logger.warning(f"No se pudo cerrar sesión de forma limpia: {e}")
