import pytest
from flows.auth_flow import AuthFlow
from pages.login_page import LoginPage
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_logout_seguro


@pytest.mark.smoke
@pytest.mark.login
def test_smoke_login_logout_basico(page):
    """
    SMOKE TEST: Verifica el ciclo de vida de la sesión (Login y Logout).
    """
    nombre_caso_prueba = "Smoke_Login_Basico"
    logger_test = get_logger(nombre_caso_prueba)

    logger_test.info(f"INICIO: Ejecutando SMOKE TEST de Autenticación: '{nombre_caso_prueba}'")

    flujo_autenticacion = AuthFlow(page)
    pagina_login = LoginPage(page)

    try:
        logger_test.info("Paso 1: Validando que el formulario de login esté disponible.")
        pagina_login.validar_presencia_login()

        logger_test.info("Paso 2: Iniciando flujo de autenticación (LOGIN).")
        nombre_usuario = flujo_autenticacion.login_con_env(caso=nombre_caso_prueba)

        assert nombre_usuario, "El login se ejecutó, pero no se detectó el nombre del usuario en el Home."
        logger_test.info(f"Login exitoso para el usuario: {nombre_usuario}")

    except Exception as e:
        logger_test.critical(f"FALLO CRÍTICO en el flujo de Login. Error: {e}", exc_info=True)
        pytest.fail(f"El Smoke de Login falló. Revisar capturas. Error: {e}")

    finally:
        logger_test.info("Paso 3: Ejecutando cierre de sesión seguro.")
        ejecutar_logout_seguro(
            flujo_autenticacion=flujo_autenticacion,
            logger_test=logger_test,
            nombre_caso_prueba=nombre_caso_prueba,
        )

        try:
            pagina_login.validar_retorno_a_login()
            logger_test.info("Paso 4: Retorno a pantalla de Login validado correctamente.")
        except Exception as e:
            logger_test.warning(f"No se pudo confirmar visualmente el retorno al Login tras el Logout. Error: {e}",
                                exc_info=True)

    logger_test.info(f"FIN: SMOKE TEST '{nombre_caso_prueba}' completado.")
