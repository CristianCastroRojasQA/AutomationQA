from typing import Optional
from playwright.sync_api import Page
from config.settings import settings
from pages.login_page import LoginPage
from utils.logger import get_logger
from utils.screenshots import capturar_evidencia


class AuthFlow:
    """
    Orquestador de alto nivel para el ciclo de vida de la sesión (Login/Logout).

    Esta clase no interactúa con selectores; coordina llamadas a Page Objects
    y gestiona la lógica de evidencias y logs de auditoría.
    """

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("AuthFlow")
        self.login_page = LoginPage(page)

    def login_con_env(self, caso: Optional[str] = None) -> str:
        """
        Inicia sesión utilizando las credenciales inyectadas por el entorno (.env).

        Args:
            caso: Nombre del test para el prefijo de evidencias.
        """
        return self.login(settings.USUARIO, settings.PASSWORD, nombre_caso=caso)

    def login(self, usuario: str, password: str, nombre_caso: Optional[str] = None) -> str:
        """
        Ejecuta el flujo completo de autenticación con validaciones de seguridad.
        """
        self.log.info(f"--- INICIO LOGIN: [{settings.PROYECTO} | {settings.AMBIENTE}] ---")

        try:
            # 1. Preparación y Validación de estado inicial
            self.login_page.validar_presencia_login()
            if nombre_caso:
                capturar_evidencia(self.page, nombre_caso, "login_01_formulario")

            # 2. Interacción técnica
            self.log.debug(f"Intentando login técnico para el usuario: '{usuario}'")
            self.login_page.ejecutar_login_tecnico(usuario, password)

            # 3. Validación de post-condición (Acceso al Home)
            user_text = self.login_page.obtener_nombre_usuario()

            if nombre_caso:
                capturar_evidencia(self.page, nombre_caso, "login_02_home")

            self.log.info(f"--- LOGIN EXITOSO: Sesión activa para [{user_text}] ---")
            return user_text

        except Exception as e:
            self.log.error(f"FALLO CRÍTICO en el proceso de Login: {str(e)}")
            if nombre_caso:
                capturar_evidencia(self.page, nombre_caso, "ERROR_LOGIN")
            raise e

    def logout(self, caso: Optional[str] = None) -> None:
        """
        Ejecuta el cierre de sesión asegurando la limpieza de la sesión en el servidor.
        """
        self.log.info("--- INICIO CIERRE DE SESIÓN (LOGOUT) ---")

        try:
            # 1. Navegación al menú de usuario
            self.login_page.abrir_menu_perfil()
            if caso:
                capturar_evidencia(self.page, caso, "logout_01_menu_abierto")

            # 2. Activación del disparador de salida
            self.log.debug("Haciendo clic en el botón de salida del menú")
            self.login_page.click_en_salir()

            # 3. Gestión de modal de confirmación
            if caso:
                capturar_evidencia(self.page, caso, "logout_02_confirmacion_intermedia")

            self.log.debug("Confirmando cierre de sesión en el modal de sistema")
            self.login_page.confirmar_cierre_sesion()

            # 4. Validación de fin de sesión (Retorno a Login)
            self.login_page.validar_retorno_a_login()

            if caso:
                capturar_evidencia(self.page, caso, "logout_03_retorno_login_ok")

            self.log.info("--- LOGOUT EXITOSO: Sesión finalizada correctamente ---")

        except Exception as e:
            # Un fallo en logout no necesariamente debe romper la suite si el test terminó, 
            # pero debe quedar registrado como advertencia técnica.
            self.log.warning(f"Logout no completado de forma estándar: {str(e)}")
            if caso:
                capturar_evidencia(self.page, caso, "ADVERTENCIA_LOGOUT")
