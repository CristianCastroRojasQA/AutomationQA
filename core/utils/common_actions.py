import pytest
from logging import Logger


def realizar_login_obligatorio(auth, nombre_test: str, logger: Logger) -> None:
    """
    Ejecuta el login de PayStudio y detiene el test si falla.

    Args:
        auth: Instancia de AuthFlow.
        nombre_test: Nombre del caso de prueba (para logs y evidencia).
        logger: Logger del test en ejecución.
    """
    logger.info(f"INICIO: Proceso de autenticación para el test: {nombre_test}")
    try:
        logger.debug("Invocando AuthFlow.login_con_env con credenciales del .env...")
        auth.login_con_env(caso=nombre_test)
        logger.info(f"FIN: Sesión establecida correctamente para el caso: {nombre_test}")
    except Exception as e:
        logger.critical(
            "DETENCIÓN: Fallo catastrófico en el Login. "
            f"El test no puede continuar sin sesión activa. Detalle: {e}"
        )
        pytest.fail("Abortando ejecución: Login fallido.")


def finalizar_sesion_segura(auth, logger: Logger, nombre_test: str) -> None:
    """
    Ejecuta el logout de PayStudio garantizando que el test no falle por este paso.

    Args:
        auth: Instancia de AuthFlow.
        logger: Logger del test en ejecución.
        nombre_test: Nombre del caso de prueba (para logs y evidencia).
    """
    logger.info("INICIO: Procedimiento de cierre de sesión seguro...")
    try:
        auth.logout(caso=nombre_test)
    except Exception as e:
        logger.warning(
            "LIMPIEZA INCOMPLETA: Se detectó un error al cerrar sesión, "
            f"pero el test se considera aprobado. Detalle: {e}"
        )
    logger.info("FIN: Sesión finalizada y recursos liberados.")
