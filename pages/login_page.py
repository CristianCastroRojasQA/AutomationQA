from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object de Login: Maneja desde el acceso hasta la confirmación de salida.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="LoginPage")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # --- LOGIN ---
        self.titulo_login = page.locator("span[id$='LabelLegend']")
        self.input_usuario = page.locator("input[id$='TextBoxUser']")
        self.input_password = page.locator("input[id$='TextBoxPassword']")
        self.btn_ingresar = page.locator("input[id$='ButtonLogInPS']")

        # --- SESIÓN ACTIVA ---
        self.opcion_salir = page.get_by_role("link", name="Salir", exact=True)

        # --- POST-LOGOUT (Confirmación) ---
        self.msg_logout_exito = page.locator("span[id$='LabelLogout']")
        self.btn_aceptar_logout = page.get_by_role("button", name="Aceptar", exact=True)

        self.log.info(f"Page Object '{self.__class__.__name__}' actualizado con controles Post-Logout.")

    # ------------------------------------------------------------------
    # Métodos de Navegación
    # ------------------------------------------------------------------
    def validar_presencia_login(self):
        self.wait_visible(self.titulo_login, desc="Título Iniciar Sesión")
        self.wait_visible(self.btn_ingresar, desc="Botón Ingresar")

    def ejecutar_login_tecnico(self, usuario: str, password: str):
        self.fill(self.input_usuario, usuario, desc="Campo Usuario")
        self.fill(self.input_password, password, desc="Campo Contraseña", mask=True)
        self.click(self.btn_ingresar, desc="Botón Ingresar")

    def click_en_salir(self):
        self.click(self.opcion_salir, desc="Click en opción Salir")

    def confirmar_cierre_sesion(self):
        """Maneja el clic en 'Aceptar' de la pantalla Post-Logout."""
        self.wait_visible(self.msg_logout_exito, desc="Mensaje 'Cerrado con éxito'")
        self.click(self.btn_aceptar_logout, desc="Botón Aceptar (Confirmación Logout)")

    def validar_retorno_a_login(self):
        self.wait_visible(self.input_usuario, desc="Input Usuario (Pantalla de Login)")
