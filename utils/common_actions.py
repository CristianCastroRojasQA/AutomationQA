from logging import Logger
import pytest


def realizar_login_obligatorio(auth, nombre_test: str, logger: Logger):
    """Ejecuta el login y detiene si falla"""

    logger.info(f"INICIO: Proceso de autenticación para el test: {nombre_test}")

    try:
        logger.debug("Invocando método de autenticación con variables de entorno (.env)...")
        auth.login_con_env(caso=nombre_test)
        logger.info(f"FIN: Sesión establecida correctamente para el caso: {nombre_test}")

    except Exception as e:
        logger.critical(
            "DETENCIÓN: Fallo catastrófico en el Login. "
            "El test no puede continuar sin sesión activa. "
            f"Detalle: {e}"
        )
        pytest.fail("Abortando ejecución: Login fallido.")


def finalizar_sesion_segura(auth, logger: Logger, nombre_test: str):
    """Cierra la sesión garantizando que el test no falle por el logout."""

    logger.info("INICIO: Procedimiento de cierre de sesión seguro...")
    try:
        auth.logout(caso=nombre_test)
    except Exception as e:
        logger.warning(
            "LIMPIEZA INCOMPLETA: Se detectó un error al cerrar sesión, "
            "pero el test se considera aprobado. "
            f"Detalle: {e}"
        )
    logger.info("FIN: Sesión finalizada y recursos liberados.")
