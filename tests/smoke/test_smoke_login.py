import pytest
from flows.auth_flow import AuthFlow
from pages.login_page import LoginPage
from utils.logger import get_logger
from utils.screenshots import capturar_evidencia


@pytest.mark.smoke
@pytest.mark.login
def test_TC_smoke_login_logout_basico(page):
    """
    SMOKE TEST: Validar el ciclo de vida básico de una sesión.
    1. Carga de la página de inicio.
    2. Login exitoso con credenciales de entorno.
    3. Verificación de presencia en Home.
    4. Cierre de sesión y retorno al login.
    """
    caso = "Smoke_Login_Logout"
    log = get_logger(caso)

    # Inicializamos los flujos y objetos de página
    auth = AuthFlow(page)
    login_pg = LoginPage(page)

    log.info("--- PASO 1: VERIFICAR DISPONIBILIDAD DE FORMULARIO ---")
    # Validamos que los inputs existan antes de intentar nada
    login_pg.validar_en_login()

    log.info("--- PASO 2: EJECUTAR LOGIN ---")
    # Utilizamos tu flujo centralizado que ya maneja logs y capturas
    nombre_usuario = auth.login_con_env(caso=caso)

    # Validación extra: Que el nombre retornado no esté vacío
    assert len(nombre_usuario) > 0, "El nombre de bienvenida está vacío o no se capturó correctamente."

    log.info("--- PASO 3: EJECUTAR LOGOUT Y CIERRE ---")
    # Cerramos sesión usando la lógica que maneja el botón 'Aceptar' opcional
    auth.logout(caso=caso)

    # Validación final: Confirmar que estamos de vuelta en la pantalla de entrada
    login_pg.validar_retorno_login()

    log.info(f"--- SMOKE TEST FINALIZADO: El acceso y salida funcionan correctamente ---")


@pytest.mark.smoke
@pytest.mark.informacion
def test_TC_smoke_verificar_version_sistema(page):
    """
    SMOKE TEST: Verificar que se puede consultar la versión del sistema.
    Esto asegura que los modales y el menú de usuario funcionan.
    """
    caso = "Smoke_Version_Sistema"
    log = get_logger(caso)

    auth = AuthFlow(page)
    login_pg = LoginPage(page)

    # Login inicial
    auth.login_con_env(caso=caso)

    log.info("--- PASO 1: ABRIR MODAL ACERCA DE ---")
    login_pg.abrir_acerca_de()

    # Capturar la versión usando tu método de Page Object
    version = login_pg.obtener_version_sistema()
    capturar_evidencia(page=page, nombre_caso=caso, nombre_paso="modal_version_visible")

    # Validación: Que la versión tenga el formato esperado (ej: contiene puntos)
    assert "." in version, f"El formato de versión detectado '{version}' no parece válido."

    log.info(f"Versión del sistema confirmada: {version}")

    login_pg.click(login_pg.btn_cerrar_modal, desc="Cerrar modal Acerca De")

    # Logout para limpiar la sesión
    auth.logout(caso=caso)
