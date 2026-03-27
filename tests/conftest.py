import pytest
from config.settings import settings
from utils.screenshots import capturar_evidencia
from utils.logger import get_logger
from flows.auth_flow import AuthFlow  # Importación del flujo refactorizado

# Inicializamos el log para el proceso de configuración
log = get_logger("Conftest")


# ======================================================================
# FIXTURES DE CONFIGURACIÓN DEL NAVEGADOR (Alcance de Sesión)
# ======================================================================

@pytest.fixture(scope="session")
def browser_name():
    """Define el motor del navegador desde el .env."""
    return settings.BROWSER


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configura los argumentos de lanzamiento del navegador."""
    return {
        **browser_type_launch_args,
        "headless": settings.HEADLESS,
        "args": ["--start-maximized"],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configura el contexto (resolución hereda del navegador maximizado)."""
    return {
        **browser_context_args,
        "viewport": None,
        "no_viewport": True,
    }


# ======================================================================
# FIXTURES DE CICLO DE VIDA (Alcance de Función)
# ======================================================================

@pytest.fixture(scope="function")
def context(browser, browser_context_args):
    """Crea un contexto aislado para cada test con headers personalizados."""
    context = browser.new_context(
        **browser_context_args,
        extra_http_headers={"Source": "AutomatedTest_PayStudio"},
    )
    context.set_default_timeout(settings.TIMEOUT)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Crea la pestaña y navega automáticamente a la URL base."""
    page = context.new_page()
    page.goto(settings.URL)
    yield page
    page.close()


@pytest.fixture(scope="function")
def auth(page):
    """
    Inyecta el flujo de autenticación.
    Permite usar 'auth' como argumento en los nuevos tests.
    """
    return AuthFlow(page)


# ======================================================================
# HOOK: CAPTURA AUTOMÁTICA DE SCREENSHOTS EN FALLOS
# ======================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Detecta fallos en la fase de ejecución y toma captura de pantalla.
    Usa 'funcargs' para ser compatible con cualquier test que use 'page'.
    """
    outcome = yield
    report = outcome.get_result()

    # Solo actuamos si el test falla durante la fase de 'call' (ejecución)
    if report.failed and call.when == "call":
        # Intentamos obtener el objeto page de los argumentos del test
        page = item.funcargs.get("page")

        if settings.SCREENSHOT_ON_FAIL and page:
            try:
                nombre_test = item.name
                # Guardamos la evidencia del error
                capturar_evidencia(page, nombre_test, "ERROR_CRITICO")
                log.error(f"Captura de pantalla guardada automáticamente por fallo en: {nombre_test}")
            except Exception as e:
                log.error(f"No se pudo realizar la captura automática en el hook: {e}")
