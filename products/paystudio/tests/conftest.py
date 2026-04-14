from typing import Generator

import pytest
from playwright.sync_api import Page, BrowserContext, Browser

from core.config.settings import settings
from core.utils.database_manager import db_manager
from core.utils.screenshots import capturar_evidencia
from core.utils.logger import get_logger
from products.paystudio.flows.auth_flow import AuthFlow

log = get_logger("Conftest.PayStudio")


# ======================================================================
# FIXTURE: LOGS DE INICIO Y FIN AUTOMATICOS
# ======================================================================

@pytest.fixture(scope="function", autouse=True)
def log_ciclo_vida_test(request) -> Generator[None, None, None]:
    """Imprime automaticamente el inicio y fin de cada caso de prueba."""
    nombre_caso = request.node.name
    logger_test = get_logger(nombre_caso)
    logger_test.info(f"INICIO: Case ID -> {nombre_caso}")
    yield
    logger_test.info(f"FIN: Ejecucion finalizada para {nombre_caso}")


# ======================================================================
# FIXTURES DE CONFIGURACION DEL NAVEGADOR (Alcance de Sesion)
# ======================================================================

@pytest.fixture(scope="session")
def browser_name() -> str:
    """Retorna el navegador configurado en settings."""
    return settings.BROWSER


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """Configura argumentos de lanzamiento del navegador."""
    return {
        **browser_type_launch_args,
        "headless": settings.HEADLESS,
        "args": ["--start-maximized"],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Configura el contexto del navegador sin viewport fijo."""
    return {
        **browser_context_args,
        "viewport": None,
        "no_viewport": True,
    }


# ======================================================================
# FIXTURES DE CICLO DE VIDA (Alcance de Funcion)
# ======================================================================

@pytest.fixture(scope="function")
def context(browser: Browser, browser_context_args: dict) -> Generator[BrowserContext, None, None]:
    """Crea un contexto de navegador para cada test."""
    context = browser.new_context(
        **browser_context_args,
        extra_http_headers={"Source": "AutomatedTest_PayStudio"},
    )
    context.set_default_timeout(settings.TIMEOUT)
    log.debug(f"Contexto de navegador creado con timeout: {settings.TIMEOUT}ms")
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Crea una pagina de Playwright navegando a la URL base."""
    page = context.new_page()
    log.info(f"Navegando a la URL base: {settings.URL}")
    page.goto(settings.URL)
    yield page
    page.close()


@pytest.fixture(scope="function")
def auth(page: Page) -> AuthFlow:
    """Retorna una instancia de AuthFlow para gestionar login/logout."""
    return AuthFlow(page)


# ======================================================================
# FIXTURES DE BASE DE DATOS
# ======================================================================

@pytest.fixture(scope="session")
def db_instance():
    """Entrega la instancia global del db_manager."""
    return db_manager


@pytest.fixture(scope="session", autouse=True)
def check_db_health(db_instance) -> bool:
    """Antes de cualquier test, verifica que la DB de PayStudio responda."""
    log.info(f"Verificando salud de la base de datos: {settings.DB_NAME}")
    if not db_instance.validar_conexion():
        log.critical(
            f"ABORTANDO: Fallo de salud en DB {settings.DB_NAME}. "
            "No se iniciara la suite de PayStudio."
        )
        pytest.exit(f"CRITICO: La base de datos '{settings.DB_NAME}' no responde.")
    return True


# ======================================================================
# FIXTURE DE SESION (Login + Logout automatico por test)
# ======================================================================

@pytest.fixture(scope="function")
def authenticated_session(
    auth: AuthFlow, page: Page, request
) -> Generator[tuple[Page, AuthFlow], None, None]:
    """
    Fixture que gestiona automaticamente login y logout para cada test.

    Elimina el boilerplate try/finally de cada caso de prueba funcional.

    Uso en tests:
        def test_mi_caso(self, authenticated_session):
            page, auth = authenticated_session
            # ... test logic sin necesidad de login/logout manual

    Yields:
        tuple[Page, AuthFlow]: Pagina activa y flujo de autenticacion.
    """
    nombre_caso = request.node.name
    logger_test = get_logger(nombre_caso)

    logger_test.info("--- PRE-CONDICION: Autenticacion automatica ---")
    auth.login_con_env(caso=nombre_caso)
    logger_test.info("--- PRE-CONDICION: Sesion establecida ---")

    yield page, auth

    logger_test.info("--- POST-CONDICION: Cierre de sesion automatico ---")
    try:
        auth.logout(caso=nombre_caso)
    except Exception as e:
        logger_test.warning(
            f"LIMPIEZA INCOMPLETA: Error al cerrar sesion en '{nombre_caso}': {e}"
        )


# ======================================================================
# HOOKS: CAPTURA AUTOMATICA EN FALLO
# ======================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar evidencia automatica si el test falla."""
    outcome = yield
    report = outcome.get_result()

    if report.failed and call.when == "call":
        page = item.funcargs.get("page")
        if settings.SCREENSHOT_ON_FAIL and page:
            log.error(
                f"FALLO DETECTADO en '{item.name}'. "
                "Iniciando protocolo de captura automatica..."
            )
            try:
                capturar_evidencia(page, item.name, "ERROR_CRITICO")
                log.info("EVIDENCIA_AUTO: Captura 'ERROR_CRITICO' generada.")
            except Exception as e:
                log.error(f"No se pudo realizar la captura automatica en el hook: {e}")
