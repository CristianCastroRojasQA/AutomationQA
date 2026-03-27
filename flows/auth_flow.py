from playwright.sync_api import Page
from config.settings import settings
from pages.login_page import LoginPage
from utils.logger import get_logger
from utils.screenshots import capturar_evidencia


class AuthFlow:
    """
    Controla el ciclo de vida de la sesión del usuario.
    """

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("AuthFlow")
        self.login_page = LoginPage(page)

    def login_con_env(self, caso: str | None = None) -> str:
        return self.login(settings.USUARIO, settings.PASSWORD, caso=caso)

    def login(self, usuario: str, password: str, caso: str | None = None) -> str:
        self.log.info("--- INICIO LOGIN ---")
        self.login_page.validar_presencia_login()

        if caso: capturar_evidencia(self.page, caso, "login_01_formulario")

        self.login_page.ejecutar_login_tecnico(usuario, password)

        user_text = self.login_page.obtener_nombre_usuario()
        if caso: capturar_evidencia(self.page, caso, "login_02_home")

        self.log.info(f"--- LOGIN EXITOSO: {user_text} ---")
        return user_text

    def logout(self, caso: str | None = None):
        """Flujo completo de salida basado en confirmación Post-Logout."""
        self.log.info("--- INICIO LOGOUT ---")

        # 1. Menú de Usuario
        self.login_page.abrir_menu_perfil()
        if caso: capturar_evidencia(self.page, caso, "logout_01_menu_abierto")

        # 2. Click en Salir
        self.login_page.click_en_salir()

        # 3. Pantalla Intermedia de Confirmación (Aceptar)
        # Aquí es donde usamos el nuevo HTML
        if caso: capturar_evidencia(self.page, caso, "logout_02_confirmacion_intermedia")
        self.login_page.confirmar_cierre_sesion()

        # 4. Verificación final de retorno al Login
        self.login_page.validar_retorno_a_login()
        if caso: capturar_evidencia(self.page, caso, "logout_03_retorno_login_ok")

        self.log.info("--- LOGOUT EXITOSO ---")
