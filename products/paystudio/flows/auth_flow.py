from typing import Optional
from playwright.sync_api import Page

from core.config.settings import settings
from core.utils.logger import get_logger
from core.utils.screenshots import capturar_evidencia
from products.paystudio.pages.login_page import LoginPage


class AuthFlow:
    """
    Orquestador de alto nivel para el ciclo de vida de la sesión (Login/Logout).

    Esta clase no interactúa con selectores. Coordina llamadas a Page Objects
    y gestiona la lógica de evidencias y logs de auditoría.
    """

    def __init__(self, page: Page):
        self.page       = page
        self.log        = get_logger("AuthFlow")
        self.login_page = LoginPage(page)

    def login_con_env(self, caso: Optional[str] = None) -> str:
        """Inicia sesión usando las credenciales inyectadas por el entorno (.env)."""
        self.log.debug(f"Extrayendo credenciales para el prefijo: {settings.PREFIX}")
        return self.login(settings.USUARIO, settings.PASSWORD, nombre_caso=caso)

    def login(self, usuario: str, password: str, nombre_caso: Optional[str] = None) -> str:
        """Ejecuta el flujo completo de autenticación con validaciones y evidencias."""
        self.log.info(f"--- INICIO LOGIN: [{settings.PROYECTO} | {settings.AMBIENTE}] ---")

        try:
            self.log.info("Paso 1: Validando disponibilidad del formulario de acceso.")
            self.login_page.validar_presencia_login()
            if nombre_caso:
                capturar_evidencia(self.page, nombre_caso, "login_01_formulario")

            self.log.debug(f"Ingresando credenciales para el usuario: '{usuario}'")
            self.login_page.ejecutar_login_tecnico(usuario, password)

            self.log.warning("Esperando sincronización de post-login")
            user_text = self.login_page.obtener_nombre_usuario()

            if nombre_caso:
                capturar_evidencia(self.page, nombre_caso, "login_02_home")

            self.log.info(f"--- LOGIN EXITOSO: Sesión activa para [{user_text}] ---")
            return user_text

        except Exception as e:
            self.log.error(
                f"LOGIN FALLIDO: No se pudo establecer sesión en {settings.URL}. Causa: {e}"
            )
            if nombre_caso:
                capturar_evidencia(self.page, nombre_caso, "ERROR_LOGIN")
            raise e

    def logout(self, caso: Optional[str] = None) -> None:
        """Ejecuta el cierre de sesión completo con validaciones."""
        self.log.info("--- INICIO CIERRE DE SESIÓN (LOGOUT) ---")

        try:
            self.login_page.abrir_menu_perfil()
            if caso:
                capturar_evidencia(self.page, caso, "logout_01_menu_abierto")

            self.login_page.click_en_salir()
            if caso:
                capturar_evidencia(self.page, caso, "logout_02_confirmacion_intermedia")

            self.login_page.confirmar_cierre_sesion()
            self.login_page.validar_retorno_a_login()

            if caso:
                capturar_evidencia(self.page, caso, "logout_03_retorno_login_ok")

            self.log.info("--- LOGOUT EXITOSO: Sesión finalizada correctamente ---")

        except Exception as e:
            self.log.warning(f"Logout incompleto: Es posible que la sesión persista. Error: {e}")
            if caso:
                capturar_evidencia(self.page, caso, "ADVERTENCIA_LOGOUT")
