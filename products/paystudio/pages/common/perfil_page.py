from datetime import datetime
from typing import Optional
from playwright.sync_api import Page
from products.paystudio.pages.base_page import BasePage
from core.utils.screenshots import capturar_evidencia


class PerfilPage(BasePage):
    """
    Gestiona las opciones de configuración y metadatos del menú de usuario.
    Incluye validaciones de fecha de negocio, versiones y seguridad.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="PerfilPage")

        # --- Fecha de Negocio ---
        self._link_trigger_fecha = page.locator("a[href='#businessDateControl']")
        self._lbl_fecha_valor = page.locator("span[id$='LabelBusinessDate']")
        self._modal_fecha = page.locator("#businessDateControl")
        self._btn_cerrar_modal_fecha = page.get_by_role("link", name="Cerrar")

        # --- Cambiar Contraseña ---
        self._link_cambiar_contrasena = page.get_by_role("link", name="Cambiar Contraseña")

        # --- Acerca de (Versión) ---
        self._link_acerca_de = page.get_by_role("link", name="Acerca de")
        self._modal_about = page.locator("#about")
        self._lbl_version_app = self._modal_about.locator("span[id$='AssemblyFileVersionAttribute']")
        self._btn_cerrar_modal_version = self._modal_about.locator("#ctl00_lblCloseButton")

    def validar_fecha_negocio_modal(self, nombre_caso: str, timeout: Optional[int] = None) -> None:
        """Valida el despliegue y consistencia de la fecha de negocio del sistema."""
        _timeout = timeout or self._title_timeout

        self.log.info(f"--- VALIDANDO FECHA DE NEGOCIO | Caso: {nombre_caso} ---")

        # Acciones de navegación
        self.abrir_menu_perfil()

        # Extracción de dato para auditoría
        self.log.debug(f"Selector fecha detectado: {self._lbl_fecha_valor}. Esperando visibilidad.")
        fecha_texto = self.get_text(self._lbl_fecha_valor, desc="Fecha en Navbar")
        self.log.info(f"Fecha detectada en sistema: {fecha_texto}")

        # Lógica de advertencia (Business Logic)
        if fecha_texto != datetime.now().strftime("%d/%m/%Y"):
            self.log.warning(
                f"ALERTA: Fecha de Negocio desincronizada. "
                f"Sistema: {fecha_texto} "
                f"Servidor: {datetime.now().strftime('%d/%m/%Y')}"
            )

        # Interacción con el modal
        self.click(self._link_trigger_fecha, desc="Trigger Modal Fecha")
        self._modal_fecha.wait_for(state="visible", timeout=_timeout)

        capturar_evidencia(self.page, nombre_caso, "Perfil_Modal_Fecha_Negocio")
        self.page.wait_for_timeout(self._animation_wait)

        # Limpieza de estado
        self.log.debug("Cerrando modal de fecha para restaurar UI.")
        self.click(self._btn_cerrar_modal_fecha, desc="Cerrar Modal Fecha")
        self._modal_fecha.wait_for(state="hidden", timeout=_timeout)

    def navegar_a_cambiar_contrasena(self, nombre_caso: str) -> None:
        """Navega al formulario de cambio de credenciales."""
        self.log.info(f"Navegando a configuración de seguridad (Cambiar Contraseña).")

        self.abrir_menu_perfil()
        self.click(self._link_cambiar_contrasena, desc="Link Cambiar Contraseña")

        capturar_evidencia(self.page, nombre_caso, "Perfil_Cambiar_Contrasena")
        self.page.wait_for_load_state("networkidle")

    def validar_version_ambiente(self, nombre_caso: str, timeout: Optional[int] = None) -> str:
        """Captura y retorna la versión técnica del aplicativo."""
        _timeout = timeout or self._title_timeout
        self.log.info("Iniciando auditoría de versión del aplicativo.")

        self.abrir_menu_perfil()
        self.click(self._link_acerca_de, desc="Opción Acerca De")

        self._modal_about.wait_for(state="visible", timeout=_timeout)

        # Extracción de la versión
        version = self.get_text(self._lbl_version_app, desc="Versión Assembly")
        self.log.info(f"--- DATOS DE AUDITORÍA --- Producto: PayStudio  Versión: {version}")

        capturar_evidencia(self.page, nombre_caso, "Modal_Version_Ambiente")

        # Cierre de modal
        self.click(self._btn_cerrar_modal_version, desc="Cerrar Acerca De")
        self._modal_about.wait_for(state="hidden", timeout=_timeout)
        self.log.debug(f"Estado del modal 'About' tras click en cerrar: {self._modal_about.is_visible()}")
        return version
