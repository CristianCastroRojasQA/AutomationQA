from playwright.sync_api import Page
from config.settings import settings
from pages.login_page import LoginPage
from utils.logger import get_logger
from utils.screenshots import capturar_evidencia


class AuthFlow:
    """
    Controla el ciclo de vida de la sesión del usuario (Login/Logout).
    Adaptado para flujos multi-proyecto y multi-ambiente.
    """

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("AuthFlow")
        self.login_page = LoginPage(page)

    def login_con_env(self, caso: str | None = None) -> str:
        """Inicia sesión usando las credenciales dinámicas del .env según Proyecto/Ambiente."""
        return self.login(settings.USUARIO, settings.PASSWORD, caso=caso)

    def login(self, usuario: str, password: str, caso: str | None = None) -> str:
        self.log.info(f"--- PASO: INICIO LOGIN [{settings.PROYECTO} - {settings.AMBIENTE}] ---")

        try:
            # 1. Validar carga inicial
            self.login_page.validar_presencia_login()
            if caso:
                capturar_evidencia(self.page, caso, "login_01_formulario")

            # 2. Ejecutar acción técnica
            self.log.info(f"Intentando login con usuario: '{usuario}'")
            self.login_page.ejecutar_login_tecnico(usuario, password)

            # 3. Validar éxito
            user_text = self.login_page.obtener_nombre_usuario()

            if caso:
                capturar_evidencia(self.page, caso, "login_02_home")

            self.log.info(f"--- PASO: LOGIN EXITOSO | Usuario detectado: {user_text} ---")
            return user_text

        except Exception as e:
            self.log.error(f"FALLO CRÍTICO en el proceso de Login: {e}")
            if caso:
                capturar_evidencia(self.page, caso, "ERROR_LOGIN")
            raise e

    def logout(self, caso: str | None = None):
        """Flujo completo de salida basado en la confirmación Post-Logout de PayStudio."""
        self.log.info("--- PASO: INICIO LOGOUT ---")

        try:
            # 1. Menú de Usuario
            self.login_page.abrir_menu_perfil()
            if caso:
                capturar_evidencia(self.page, caso, "logout_01_menu_abierto")

            # 2. Click en Salir
            self.login_page.click_en_salir()

            # 3. Pantalla Intermedia de Confirmación (Click en 'Aceptar')
            if caso:
                capturar_evidencia(self.page, caso, "logout_02_confirmacion_intermedia")

            self.log.info("Confirmando cierre de sesión en modal...")
            self.login_page.confirmar_cierre_sesion()

            # 4. Verificación final de retorno al Login
            self.login_page.validar_retorno_a_login()

            if caso:
                capturar_evidencia(self.page, caso, "logout_03_retorno_login_ok")

            self.log.info("--- PASO: LOGOUT EXITOSO ---")

        except Exception as e:
            self.log.warning(f"El proceso de logout no fue limpio o ya se había cerrado la sesión: {e}")
            if caso:
                capturar_evidencia(self.page, caso, "ADVERTENCIA_LOGOUT")
