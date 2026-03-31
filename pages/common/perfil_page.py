from datetime import datetime

from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.screenshots import capturar_evidencia


class PerfilPage(BasePage):
    """
    Maneja las opciones del menú de usuario.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="PerfilPage")

        # Fecha de Negocio
        self.link_trigger_fecha = page.locator("a[href='#businessDateControl']")
        self.lbl_fecha_valor = page.locator("span[id$='LabelBusinessDate']")
        self.modal_fecha = page.locator("#businessDateControl")
        self.btn_cerrar_modal_fecha = page.get_by_role("link", name="Cerrar")

        # Cambiar Contraseña
        self.link_cambiar_contrasena = page.get_by_role(role="link", name="Cambiar Contraseña")

        # Acerca de
        self.link_acerca_de = page.get_by_role(role="link", name="Acerca de")
        self.modal_about = page.locator("#about")
        self.lbl_version_app = self.modal_about.locator("span[id$='AssemblyFileVersionAttribute']")
        self.btn_cerrar_modal_version = self.modal_about.locator("#ctl00_lblCloseButton")

    def validar_fecha_negocio_modal(self, nombre_caso: str, timeout: int = None):
        """Valida que el modal de fecha de negocio se despliegue correctamente."""
        timeout = timeout or self.TITLE_TIMEOUT
        self.log.info(f"Iniciando navegación a 'Fecha de Negocio' para el caso: '{nombre_caso}'.")

        # 1. Abrir el menú de usuario
        self.log.info("Abriendo menú de perfil del usuario.")
        self.abrir_menu_perfil()

        self.log.info("Esperando que el enlace de Fecha de Negocio esté visible.")
        self.wait_visible(self.link_trigger_fecha, desc="Link de Fecha")

        # 2. Capturar texto antes de hacer clic (para el log)
        fecha_texto = self.lbl_fecha_valor.inner_text().strip()
        self.log.info(f"FECHA DE NEGOCIO ACTUAL: {fecha_texto}")
        if self.lbl_fecha_valor.inner_text().strip() != datetime.now().strftime("%d/%m/%Y"):
            self.log.warning("LA FECHA DE NEGOCIO NO COINCIDE CON LA FECHA ACTUAL")

        # 3. Hacer clic en la fecha para abrir el modal
        self.log.info("Haciendo clic en el enlace de Fecha de Negocio para abrir el modal.")
        self.click(self.link_trigger_fecha, desc="Trigger del Modal de Fecha")

        # 4. Esperar a que el modal sea visible
        self.log.info("Esperando a que el modal de Fecha de Negocio sea visible.")
        self.modal_fecha.wait_for(state="visible", timeout=timeout)
        self.log.info("Modal 'businessDateControl' desplegado exitosamente.")

        capturar_evidencia(self.page, nombre_caso, "Perfil_Modal_Fecha_Negocio")
        self.log.info("Evidencia capturada: Modal de Fecha de Negocio visible.")

        self.page.wait_for_timeout(self.ANIMATION_WAIT)

        # 5. Cerrar el modal
        self.log.debug("Cerrando modal de Fecha de Negocio para limpiar el estado del test.")
        self.btn_cerrar_modal_fecha.click()

        self.modal_fecha.wait_for(state="hidden", timeout=timeout)
        self.log.info("Modal de Fecha de Negocio cerrado correctamente. Flujo finalizado.")

    def navegar_a_cambiar_contrasena(self, nombre_caso: str):
        self.log.info(f"Iniciando navegación a 'Cambiar Contraseña' para el caso: '{nombre_caso}'.")

        self.log.info("Abriendo menú de perfil del usuario.")
        self.abrir_menu_perfil()

        self.log.info("Haciendo clic en el enlace de Cambiar Contraseña.")
        self.click(self.link_cambiar_contrasena, desc="Cambiar Contraseña")

        capturar_evidencia(self.page, nombre_caso, "Perfil_Cambiar_Contraseña")
        self.log.info("Evidencia capturada: Perfil_Cambiar Contraseña")

        self.page.wait_for_timeout(self.ANIMATION_WAIT)

        self.page.wait_for_load_state("networkidle")
        self.wait_visible(self.user_welcome, desc="User Welcome en nueva página")

    def validar_version_ambiente(self, nombre_caso: str, timeout: int = None):
        """Captura y valida la versión del sistema en el modal Acerca De."""
        timeout = timeout or self.TITLE_TIMEOUT
        self.log.info("Iniciando captura de versión del ambiente (Acerca De).")

        self.log.info("Abriendo menú de perfil del usuario.")
        self.abrir_menu_perfil()

        # 2. Clic en la opción Acerca De
        self.log.info("Esperando a que el modal de Acerca de sea visible.")
        self.click(self.link_acerca_de, desc="Opción Acerca De")

        # 3. Esperar a que el modal sea visible
        self.modal_about.wait_for(state="visible", timeout=timeout)
        self.log.info("Modal 'Acerca De' desplegado.")

        # 4. Extraer el texto de la versión
        version = self.lbl_version_app.inner_text().strip()
        self.log.info(f"VERSIÓN DETECTADA: {version}")

        # 5. Evidencia y Espera Visual
        self.log.info("Evidencia capturada: Modal de Acerca de visible.")
        capturar_evidencia(self.page, nombre_caso, "Modal_Version_Ambiente")

        self.log.info("Manteniendo modal de versión abierto por 2 segundos...")
        self.page.wait_for_timeout(self.ANIMATION_WAIT * 2)

        # 6. Cerrar y Limpiar
        self.btn_cerrar_modal_version.click()
        self.modal_about.wait_for(state="hidden", timeout=timeout)
