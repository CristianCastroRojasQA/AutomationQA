from playwright.sync_api import Page
from config.settings import settings
from pages.login_page import LoginPage
from utils.logger import get_logger
from utils.screenshots import capturar_evidencia


class AuthFlow:
    """
    AuthFlow centraliza el proceso de autenticación:
    - login (con env o con credenciales directas)
    - validación de home
    - logout (con confirmación opcional 'Aceptar' si aparece)

    Mantiene el framework escalable porque evita repetir pasos en cada test.
    """

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("AuthFlow")
        self.login_page = LoginPage(page)

    # -------------------------
    # LOGIN
    # -------------------------
    def login_con_env(self, caso: str | None = None) -> str:
        """
        Login usando credenciales desde .env (settings.USUARIO/settings.PASSWORD).
        Retorna el texto del welcome (UserWelcome).
        """
        return self.login(settings.USUARIO, settings.PASSWORD, caso=caso)

    def login(self, usuario: str, password: str, caso: str | None = None) -> str:
        """
        Login con credenciales explícitas.
        Si 'caso' se provee, toma evidencias con tu formato actual.
        Retorna el texto del welcome (UserWelcome).
        """
        self.log.info("INICIO - Login")

        # Validar que estamos en login (inputs/botón visibles)
        self.login_page.validar_en_login()
        if caso:
            capturar_evidencia(self.page, caso, "01_login_visible")

        # Ejecutar login
        self.log.info(f"Login con usuario: {usuario}")
        self.login_page.login(usuario, password)

        # Validar home
        welcome_text = self.login_page.validar_home()
        self.log.info(f"Login OK. Welcome: {welcome_text}")

        if caso:
            capturar_evidencia(self.page, caso, "02_home_visible")

        self.log.info("FIN - Login OK")
        return welcome_text

    # -------------------------
    # LOGOUT
    # -------------------------
    def logout(self, caso: str | None = None):
        """
        Logout:
        - Click dropdown usuario
        - Click 'Salir'
        - Si aparece botón 'Aceptar', lo presiona
        - Valida retorno al login
        """
        self.log.info("INICIO - Logout")

        # Salir (dropdown + opción salir)
        self.login_page.salir()

        # Confirmación opcional (Aceptar)
        acepto = self.login_page.confirmar_logout_si_aparece()
        if acepto:
            self.log.info("Se mostró confirmación de cierre y se presionó 'Aceptar'.")
        else:
            self.log.info("No apareció confirmación 'Aceptar'.")

        # Validar retorno a login
        self.login_page.validar_retorno_login()
        self.log.info("Logout OK: regresó al login.")

        if caso:
            capturar_evidencia(self.page, caso, "03_logout_ok")

        self.log.info("FIN - Logout OK")
