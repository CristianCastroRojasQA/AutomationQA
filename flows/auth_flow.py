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
        # Referencia a la página activa para interactuar con el navegador
        self.page = page
        # Inicializa el logger específico para el flujo de autenticación
        self.log = get_logger("AuthFlow")
        # Instancia el Page Object de Login para acceder a sus métodos técnicos
        self.login_page = LoginPage(page)

    # -------------------------
    # LOGIN
    # -------------------------
    def login_con_env(self, caso: str | None = None) -> str:
        """
        Realiza el login extrayendo las credenciales automáticamente del archivo .env.
        Retorna el nombre del usuario detectado en el Home (UserWelcome).
        """
        # Reutiliza el método login() enviando los datos cargados en el objeto settings
        return self.login(settings.USUARIO, settings.PASSWORD, caso=caso)

    def login(self, usuario: str, password: str, caso: str | None = None) -> str:
        """
        Flujo completo de inicio de sesión con captura de evidencias paso a paso.
        @param usuario: Username a ingresar.
        @param password: Password a ingresar.
        @param caso: Nombre del caso de prueba para organizar las capturas de pantalla.
        """
        self.log.info("INICIO - Login")

        # Paso 1: Asegura que la página cargó los inputs antes de intentar escribir
        self.login_page.validar_en_login()
        if caso:
            # Captura evidencia de que el formulario de login está presente
            capturar_evidencia(self.page, caso, "01_login_visible")

        # Paso 2: Ejecuta la acción técnica de llenar campos y presionar 'Ingresar'
        self.log.info(f"Login con usuario: {usuario}")
        self.login_page.login(usuario, password)

        # Paso 3: Verifica que el login fue exitoso buscando el mensaje de bienvenida
        welcome_text = self.login_page.validar_home()
        self.log.info(f"Login OK. Welcome: {welcome_text}")

        if caso:
            # Captura evidencia del estado exitoso dentro de la aplicación
            capturar_evidencia(self.page, caso, "02_home_visible")

        self.log.info("FIN - Login OK")
        return welcome_text

    # -------------------------
    # LOGOUT
    # -------------------------
    def logout(self, caso: str | None = None):
        """
        Flujo completo de cierre de sesión, manejando pasos opcionales y validación final.
        """
        self.log.info("INICIO - Logout")

        # Paso 1: Abre el menú de usuario y presiona el enlace técnico de salida
        self.login_page.salir()

        # Paso 2: Maneja la pantalla de confirmación intermedia de ASP.NET (si aparece)
        # Esto previene que el test falle si la aplicación a veces pide confirmación y otras no
        acepto = self.login_page.confirmar_logout_si_aparece()
        if acepto:
            self.log.info("Se mostró confirmación de cierre y se presionó 'Aceptar'.")
        else:
            self.log.info("No apareció confirmación 'Aceptar'.")

        # Paso 3: Aserción final para confirmar que el sistema expulsó al usuario correctamente
        self.login_page.validar_retorno_login()
        self.log.info("Logout OK: regresó al login.")

        if caso:
            # Captura la evidencia final del proceso de logout
            capturar_evidencia(self.page, caso, "03_logout_ok")

        self.log.info("FIN - Logout OK")
