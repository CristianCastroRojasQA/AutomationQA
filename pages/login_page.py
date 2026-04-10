from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object Model para el módulo de Autenticación.

    Gestiona los elementos y acciones desde el formulario de acceso inicial 
    hasta los flujos de confirmación de salida y limpieza de sesión.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="LoginPage")

        # --- Locators: Formulario de Login ---
        self._titulo_login = page.locator("span[id$='LabelLegend']")
        self._input_usuario = page.locator("input[id$='TextBoxUser']")
        self._input_password = page.locator("input[id$='TextBoxPassword']")
        self._btn_ingresar = page.locator("input[id$='ButtonLogInPS']")

        # --- Locators: Sesión Activa / Perfil ---
        self._opcion_salir = page.get_by_role("link", name="Salir", exact=True)

        # --- Locators: Post-Logout (Workflow de confirmación) ---
        self._msg_logout_exito = page.locator("span[id$='LabelLogout']")
        self._btn_aceptar_logout = page.get_by_role("button", name="Aceptar", exact=True)

        self.log.debug(f"Locators para {self.__class__.__name__} inicializados correctamente.")

    # --- Acciones de Validación de Estado ---

    def validar_presencia_login(self) -> None:
        """Verifica que los elementos críticos del login estén listos para interactuar."""
        self.log.debug("Validando presencia de componentes de login...")
        self.wait_visible(self._titulo_login, desc="Título Iniciar Sesión")
        self.wait_visible(self._btn_ingresar, desc="Botón Ingresar")

    def validar_retorno_a_login(self) -> None:
        """Confirma que el flujo de salida terminó exitosamente en la pantalla de acceso."""
        self.log.debug("Validando redirección a pantalla de login tras logout.")
        self.wait_visible(self._input_usuario, desc="Input Usuario (Post-Logout)")

    # --- Acciones de Interacción ---

    def ejecutar_login_tecnico(self, usuario: str, password: str) -> None:
        """
        Ejecuta la secuencia de ingreso de credenciales y envío del formulario.
        """
        self.log.info(f"Ejecutando proceso de ingreso para el usuario: {usuario}")
        self.fill(self._input_usuario, usuario, desc="Campo Usuario")
        self.fill(self._input_password, password, desc="Campo Contraseña", mask=True)
        self.click(self._btn_ingresar, desc="Botón Ingresar")

    def click_en_salir(self) -> None:
        """Inicia el proceso de logout desde el menú de usuario."""
        self.log.debug("Intentando clic en la opción 'Salir' del menú.")
        self.click(self._opcion_salir, desc="Vínculo Salir")

    def confirmar_cierre_sesion(self) -> None:
        """
        Maneja la pantalla intermedia de confirmación propia de PayStudio.
        Espera el mensaje de éxito y confirma el cierre definitivo.
        """
        self.log.debug("Esperando pantalla de confirmación post-logout.")
        self.wait_visible(self._msg_logout_exito, desc="Mensaje 'Sesión cerrada con éxito'")
        self.click(self._btn_aceptar_logout, desc="Botón Aceptar (Confirmación Logout)")
