from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object de Login: Define los elementos y acciones de la pantalla de acceso
    y el encabezado (Header) del sistema.
    """

    def __init__(self, page: Page):
        # Llama al constructor de BasePage para heredar el driver 'page' y el logger
        super().__init__(page, logger_name="LoginPage")

        # ===================================================================
        # SELECTORES DE LA PÁGINA DE LOGIN
        # ===================================================================

        # Selector de atributo parcial ($=): Busca el span cuyo ID termina en 'LabelLegend'
        # Es robusto contra prefijos dinámicos de servidores ASP.NET (ej: ctl00_...)
        self.titulo_login = page.locator("span[id$='LabelLegend']")

        # Input de Usuario: Localiza el campo de texto finalizando en 'TextBoxUser'
        self.input_usuario = page.locator("input[id$='TextBoxUser']")

        # Input de Password: Localiza el campo de contraseña finalizando en 'TextBoxPassword'
        self.input_password = page.locator("input[id$='TextBoxPassword']")

        # Botón Ingresar: Localiza el input de tipo botón que termina en 'ButtonLogInPS'
        self.btn_ingresar = page.locator("input[id$='ButtonLogInPS']")

        # ===================================================================
        # SELECTORES DE HOME Y SESIÓN (HEADER)
        # ===================================================================

        # Elemento que muestra el nombre del usuario logueado al finalizar el login
        self.user_welcome = page.locator("span[id$='UserWelcome']")

        # XPATH Ancestor: Localiza el enlace <a> que es padre directo o abuelo del nombre de usuario
        # Esto es necesario para poder hacer clic y desplegar el menú de opciones de cuenta
        self.user_dropdown: Locator = self.user_welcome.locator("xpath=ancestor::a[1]")

        # Opción Salir: Busca el enlace técnico de logout mediante el final de su ID
        self.opcion_salir = page.locator("a[id$='LinkButtonLogOff']")

        # Botón Confirmar: Botón 'Aceptar' que aparece en la pantalla intermedia de cierre de sesión
        self.btn_confirmar_logout = page.locator("input[id$='ButtonOk']")

    # -------------------------
    # Validaciones y acciones
    # -------------------------

    def validar_en_login(self):
        """Verifica que todos los elementos críticos del login estén visibles en pantalla."""
        self.wait_visible(self.titulo_login, desc="Título: Iniciar sesión")
        self.wait_visible(self.input_usuario, desc="Input Usuario")
        self.wait_visible(self.input_password, desc="Input Contraseña")
        self.wait_visible(self.btn_ingresar, desc="Botón Ingresar")

    def login(self, usuario: str, password: str):
        """Realiza el proceso técnico de ingresar credenciales y enviar el formulario."""
        self.fill(self.input_usuario, usuario, desc="Campo Usuario")
        # Se usa mask=True para que la contraseña no quede escrita en los logs del framework
        self.fill(self.input_password, password, desc="Campo Contraseña", mask=True)
        self.click(self.btn_ingresar, desc="Botón Ingresar")

    def validar_home(self) -> str:
        """Valida la entrada exitosa al sistema y devuelve el nombre del usuario detectado."""
        self.wait_visible(self.user_welcome, desc="UserWelcome (post-login)")
        return self.user_welcome.inner_text().strip()

    def salir(self):
        """Ejecuta el flujo de salida: abre el menú de usuario y presiona 'Salir'."""
        # Primero hace clic en el nombre para expandir el dropdown
        self.click(self.user_dropdown, desc="Dropdown usuario (UserWelcome)")
        # Espera que la animación del menú termine antes de intentar el clic en 'Salir'
        self.wait_visible(self.opcion_salir, desc="Opción Salir (dropdown abierto)")
        self.click(self.opcion_salir, desc="Opción Salir")

    def confirmar_logout_si_aparece(self, timeout_ms: int = 3000) -> bool:
        """
        Maneja la pantalla intermedia de confirmación de logout.
        Usa un bloque try/except para que el test no falle si la pantalla no aparece.
        """
        try:
            # Intenta esperar el botón con un tiempo corto (3 seg por defecto)
            self.btn_confirmar_logout.wait_for(state="visible", timeout=timeout_ms)
            self.click(self.btn_confirmar_logout, desc="Botón Aceptar cierre sesión")
            return True
        except Exception:
            # Si el tiempo expira y el botón no está, se asume que la sesión cerró directo
            return False

    def validar_retorno_login(self):
        """Aserción final para confirmar que el navegador regresó a la pantalla de acceso."""
        self.wait_visible(self.input_usuario, desc="Input Usuario (de vuelta en login)")
