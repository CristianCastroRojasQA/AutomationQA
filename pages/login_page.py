from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object básico: Login + Home + Logout.
    ASP.NET legacy: usamos IDs estables.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="LoginPage")

        # ===================================================================
        # LOGIN PAGE SELECTORS
        # ===================================================================
        
        # ADVERTENCIA: Los selectores de texto (get_by_text) son frágiles.
        # Si el idioma o el texto cambia, los tests fallarán.
        # Preferir: data-testid, aria-label, o IDs cuando sea posible.
        
        # Título de login (frágil: depende del texto exacto)
        self.titulo_login: Locator = page.get_by_text("Iniciar sesión")
        
        # Selectores por ID (robustos: independientes de cambios de UI)
        self.input_usuario: Locator = page.locator(
            "#ctl00_CphContent_LoginControl1_TextBoxUser"
        )
        self.input_password: Locator = page.locator(
            "#ctl00_CphContent_LoginControl1_TextBoxPassword"
        )
        self.btn_ingresar: Locator = page.locator(
            "#ctl00_CphContent_LoginControl1_ButtonLogInPS"
        )

        # Home (span con el nombre del usuario, por ID)
        self.user_welcome: Locator = page.locator("#ctl00_HeaderControl1_UserWelcome")

        # Dropdown usuario = <a> que contiene el span UserWelcome (robusto con xpath)
        self.user_dropdown: Locator = self.user_welcome.locator("xpath=ancestor::a[1]")

        # Opción "Salir" (frágil: depende del texto exacto)
        # TODO: Reemplazar con selector por data-testid si está disponible
        self.opcion_salir: Locator = page.get_by_text("Salir", exact=True)

        # Pantalla intermedia de logout: botón OK "Aceptar" (robusto: por ID)
        self.btn_logout_ok: Locator = page.locator(
            "#ctl00_CphContent_LogoutControl1_ButtonOk"
        )

    # -------------------------
    # Validaciones y acciones
    # -------------------------
    def validar_en_login(self):
        self.wait_visible(self.titulo_login, desc="Título: Iniciar sesión")
        self.wait_visible(self.input_usuario, desc="Input Usuario")
        self.wait_visible(self.input_password, desc="Input Contraseña")
        self.wait_visible(self.btn_ingresar, desc="Botón Ingresar")

    def login(self, usuario: str, password: str):
        self.fill(self.input_usuario, usuario, desc="Campo Usuario")
        self.fill(self.input_password, password, desc="Campo Contraseña", mask=True)
        self.click(self.btn_ingresar, desc="Botón Ingresar")

    def validar_home(self) -> str:
        self.wait_visible(self.user_welcome, desc="UserWelcome (post-login)")
        return self.user_welcome.inner_text().strip()

    def salir(self):
        """Abre dropdown del usuario y hace clic en 'Salir'."""
        self.click(self.user_dropdown, desc="Dropdown usuario (UserWelcome)")
        # Esperar a que la opción "Salir" sea visible antes de hacer click
        self.wait_visible(self.opcion_salir, desc="Opción Salir (dropdown abierto)")
        self.click(self.opcion_salir, desc="Opción Salir")

    def confirmar_logout_si_aparece(self, timeout_ms: int = 3000) -> bool:
        """
        Si aparece la pantalla intermedia con botón 'Aceptar', lo presiona.
        Retorna True si lo presionó, False si no apareció.
        """
        try:
            self.btn_logout_ok.wait_for(state="visible", timeout=timeout_ms)
            self.click(self.btn_logout_ok, desc="Botón Aceptar cierre sesión")
            return True
        except Exception:
            # No apareció el botón, no pasa nada
            return False

    def validar_retorno_login(self):
        """Valida que volvimos al login."""
        self.wait_visible(self.input_usuario, desc="Input Usuario (de vuelta en login)")
