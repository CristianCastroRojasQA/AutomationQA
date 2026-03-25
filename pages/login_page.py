from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object de Login.
    Responsable ÚNICAMENTE del flujo básico:
    - Disponibilidad del login
    - Autenticación
    - Confirmación de sesión activa
    - Cierre de sesión
    - Retorno al login

    Usado EXCLUSIVAMENTE por pruebas Smoke de Login.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="LoginPage")

        # =============================================================
        # SELECTORES DE LOGIN
        # =============================================================

        self.titulo_login = page.locator("span[id$='LabelLegend']")
        self.input_usuario = page.locator("input[id$='TextBoxUser']")
        self.input_password = page.locator("input[id$='TextBoxPassword']")
        self.btn_ingresar = page.locator("input[id$='ButtonLogInPS']")

        # =============================================================
        # SELECTORES DE SESIÓN (POST-LOGIN)
        # =============================================================

        self.user_welcome = page.locator("span[id$='UserWelcome']")
        self.user_dropdown: Locator = self.user_welcome.locator("xpath=ancestor::a[1]")
        self.opcion_salir = page.locator("a[id$='LinkButtonLogOff']")
        self.btn_confirmar_logout = page.locator("input[id$='ButtonOk']")

    # =============================================================
    # ACCIONES Y VALIDACIONES SMOKE LOGIN
    # =============================================================

    def validar_en_login(self):
        """Valida que el formulario de login esté visible y disponible."""
        self.wait_visible(self.titulo_login, desc="Título Login")
        self.wait_visible(self.input_usuario, desc="Input Usuario")
        self.wait_visible(self.input_password, desc="Input Contraseña")
        self.wait_visible(self.btn_ingresar, desc="Botón Ingresar")

    def login(self, usuario: str, password: str):
        """Ejecuta el login técnico con credenciales."""
        self.fill(self.input_usuario, usuario, desc="Campo Usuario")
        self.fill(self.input_password, password, desc="Campo Contraseña", mask=True)
        self.click(self.btn_ingresar, desc="Botón Ingresar")

    def validar_home(self) -> str:
        """
        Confirma que la sesión quedó activa.
        Devuelve el nombre del usuario logueado.
        """
        self.wait_visible(self.user_welcome, desc="UserWelcome visible")
        return self.user_welcome.inner_text().strip()

    def abrir_menu_usuario(self):
        """Abre el dropdown del usuario (menú de sesión)."""
        self.click(self.user_dropdown, desc="Abrir menú usuario")

    def click_salir(self):
        """Hace clic en la opción 'Salir' del dropdown."""
        self.wait_visible(self.opcion_salir, desc="Opción Salir visible (menú abierto)")
        self.click(self.opcion_salir, desc="Click en Salir")

    def salir(self):
        """Ejecuta el cierre de sesión desde el menú de usuario."""
        self.click(self.user_dropdown, desc="Abrir menú usuario")
        self.wait_visible(self.opcion_salir, desc="Opción Salir visible")
        self.click(self.opcion_salir, desc="Click en Salir")

    def confirmar_logout_si_aparece(self, timeout_ms: int = 3000) -> bool:
        """
        Maneja pantalla opcional de confirmación de logout.
        No falla el test si no aparece.
        """
        try:
            self.btn_confirmar_logout.wait_for(state="visible", timeout=timeout_ms)
            self.click(self.btn_confirmar_logout, desc="Confirmar cierre sesión")
            return True
        except Exception:
            return False

    def validar_retorno_login(self):
        """Confirma que el navegador regresó a la pantalla de login."""
        self.wait_visible(self.input_usuario, desc="Login visible nuevamente")