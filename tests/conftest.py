import pytest
from config.settings import settings
from utils.screenshots import capturar_evidencia
from utils.logger import get_logger

log = get_logger("Conftest")

# ======================================================================
# HOOKS DE PYTEST - CAPTURA AUTOMÁTICA DE FALLOS
# ======================================================================


@pytest.fixture(scope="session")
def browser_name():
    return settings.BROWSER


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": settings.HEADLESS,
        "args": ["--start-maximized"],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": None,
        "no_viewport": True,
    }


@pytest.fixture(scope="function")
def context(browser, browser_context_args):
    context = browser.new_context(
        **browser_context_args,
        extra_http_headers={"Source": "AutomatedTest_GetNet"},
    )
    context.set_default_timeout(settings.TIMEOUT)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context, request):
    """Fixture de página con soporte para captura automática en fallos."""
    page = context.new_page()
    page.goto(settings.URL)
    
    # Guardar referencia al page en request para acceso en hooks
    request.page = page
    
    yield page
    page.close()


# ======================================================================
# HOOK: CAPTURA AUTOMÁTICA DE SCREENSHOTS EN FALLOS
# ======================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook que captura automáticamente screenshot e información de fallos.
    Ejecuta después de cada fase de test (setup, call, teardown).
    """
    outcome = yield
    report = outcome.get_result()
    
    # Solo procesar si la prueba falló en la fase de ejecución (call)
    if report.failed and call.when == "call":
        if settings.SCREENSHOT_ON_FAIL and hasattr(item, "page"):
            try:
                nombre_test = item.name
                capturar_evidencia(item.page, nombre_test, "FALLO_screenshot")
                log.error(f"Screenshot de fallo guardado para: {nombre_test}")
            except Exception as e:
                log.error(f"No se pudo capturar screenshot en fallo: {e}")
