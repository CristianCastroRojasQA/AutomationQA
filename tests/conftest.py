import pytest
from config.settings import settings
from utils.database_manager import db_manager
from utils.screenshots import capturar_evidencia
from utils.logger import get_logger
from flows.auth_flow import AuthFlow

# Inicializamos el log para el proceso de configuración del framework
log = get_logger("Conftest")


# ======================================================================
# FIXTURE: LOGS DE INICIO Y FIN AUTOMÁTICOS
# ======================================================================

@pytest.fixture(scope="function", autouse=True)
def log_ciclo_vida_test(request):
    """
    Imprime automáticamente el inicio y fin de cada caso de prueba.
    autouse=True hace que se ejecute en todos los tests sin invocarlo.
    """
    nombre_caso = request.node.name
    logger_test = get_logger(nombre_caso)

    # Mensaje de Inicio
    logger_test.info(f"INICIO: Ejecutando {nombre_caso}")

    yield

    # El estado final lo determinamos según el reporte de pytest
    # Si llegamos aquí sin excepciones, el flujo fue exitoso.
    logger_test.info(f"PRUEBA FINALIZADA CON ÉXITO: {nombre_caso}")


# ======================================================================
# FIXTURES DE CONFIGURACIÓN DEL NAVEGADOR (Alcance de Sesión)
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


# ======================================================================
# FIXTURES DE CICLO DE VIDA (Alcance de Función)
# ======================================================================

@pytest.fixture(scope="function")
def context(browser, browser_context_args):
    context = browser.new_context(
        **browser_context_args,
        extra_http_headers={"Source": "AutomatedTest_PayStudio"},
    )
    context.set_default_timeout(settings.TIMEOUT)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    page.goto(settings.URL)
    yield page
    page.close()


@pytest.fixture(scope="function")
def auth(page):
    return AuthFlow(page)


# ======================================================================
# FIXTURES DE BASE DE DATOS
# ======================================================================

@pytest.fixture(scope="session")
def db_instance():
    """Entrega la instancia global del db_manager."""
    return db_manager


@pytest.fixture(scope="session", autouse=True)
def check_db_health(db_instance):
    """Antes de cualquier test, verifica que la DB responda."""
    log.info(f"Verificando salud de la base de datos: {settings.DB_NAME}")
    if not db_instance.validar_conexion():
        pytest.exit(f"CRÍTICO: La base de datos '{settings.DB_NAME}' no responde. Abortando ejecución.")
    return True


# ======================================================================
# HOOKS: CAPTURA AUTOMÁTICA Y REPORTES
# ======================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar evidencia si el test falla."""
    outcome = yield
    report = outcome.get_result()

    if report.failed and call.when == "call":
        page = item.funcargs.get("page")
        if settings.SCREENSHOT_ON_FAIL and page:
            try:
                nombre_test = item.name
                capturar_evidencia(page, nombre_test, "ERROR_CRITICO")
                log.error(f"Captura de pantalla guardada automáticamente por fallo en: {nombre_test}")
            except Exception as e:
                log.error(f"No se pudo realizar la captura automática en el hook: {e}")
