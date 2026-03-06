import pytest
from config.settings import settings
from utils.screenshots import capturar_evidencia
from utils.logger import get_logger

# Inicializamos el log para el proceso de configuración de los tests
log = get_logger("Conftest")


# ======================================================================
# FIXTURES DE CONFIGURACIÓN DEL NAVEGADOR (Alcance de Sesión)
# ======================================================================


@pytest.fixture(scope="session")
def browser_name():
    """Define el motor del navegador (chromium, firefox, webkit) desde el .env."""
    return settings.BROWSER


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configura los argumentos de lanzamiento del navegador."""
    return {
        **browser_type_launch_args,
        "headless": settings.HEADLESS,  # Ejecuta con o sin interfaz gráfica
        "args": ["--start-maximized"],  # Inicia el navegador ocupando toda la pantalla
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configura el contexto del navegador (resolución, geolocalización, etc)."""
    return {
        **browser_context_args,
        "viewport": None,  # Desactiva el tamaño de ventana por defecto
        "no_viewport": True,  # Permite que herede el tamaño del navegador maximizado
    }


# ======================================================================
# FIXTURES DE CICLO DE VIDA (Alcance de Función)
# ======================================================================


@pytest.fixture(scope="function")
def context(browser, browser_context_args):
    """
    Crea un contexto aislado para cada test.
    Esto evita que las cookies o el caché de un test afecten al siguiente.
    """
    context = browser.new_context(
        **browser_context_args,
        # Inyecta un encabezado HTTP para identificar el tráfico automatizado
        extra_http_headers={"Source": "AutomatedTest_GetNet"},
    )
    # Define el tiempo máximo de espera para cada acción dentro del contexto
    context.set_default_timeout(settings.TIMEOUT)
    yield context  # Aquí es donde se ejecuta el test
    context.close()  # Cierre de seguridad después de cada test


@pytest.fixture(scope="function")
def page(context, request):
    """
    Crea la pestaña (Page) donde ocurrirá la interacción.
    Navega automáticamente a la URL base configurada.
    """
    page = context.new_page()
    page.goto(settings.URL)  # Navegación inicial automática

    # IMPORTANTE: Adjuntamos el objeto 'page' al objeto 'request'.
    # Esto permite que el Hook de fallos pueda acceder a la pestaña para tomar la foto.
    request.page = page

    yield page  # El test usa este objeto para sus interacciones
    page.close()


# ======================================================================
# HOOK: CAPTURA AUTOMÁTICA DE SCREENSHOTS EN FALLOS
# ======================================================================


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook avanzado de Pytest que intercepta el resultado de cada prueba.
    Si el test falla, dispara la captura de evidencia automáticamente.
    """
    # Ejecuta la fase del test (setup, call o teardown)
    outcome = yield
    report = outcome.get_result()

    # Verificamos si la fase de ejecución ('call') resultó en fallo
    if report.failed and call.when == "call":
        # Verificamos si tenemos acceso a la página y si la opción de captura está activa
        if settings.SCREENSHOT_ON_FAIL and hasattr(item, "page"):
            try:
                nombre_test = item.name  # Nombre exacto del test fallido
                # Llama a la utilidad de screenshots para guardar la evidencia del error
                capturar_evidencia(item.page, nombre_test, "FALLO_screenshot")
                log.error(f"Screenshot de fallo guardado para: {nombre_test}")
            except Exception as e:
                log.error(f"No se pudo capturar screenshot en fallo: {e}")
