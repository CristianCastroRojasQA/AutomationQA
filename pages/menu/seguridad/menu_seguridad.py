from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import Callable


class MenuSeguridadPage(BasePage):
    """
    Clase base para la página del menú principal de Seguridad.
    Proporciona métodos para interactuar con el menú de nivel superior
    y una función genérica para la navegación a subpáginas.
    """

    def __init__(self, page: Page, logger_name: str = "MenuSeguridad"):
        super().__init__(page, logger_name=logger_name)
        # Nivel 1: Menú Principal
        self.link_menu_principal_seguridad = page.get_by_role("link", name="Seguridad")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

    def abrir_menu_seguridad(self):
        self.log.info("[NAV] Desplegando menú principal de Seguridad (#SECURITY_KEY)")
        self.log.debug("Esperando que el menú de seguridad sea interactuable (Clickable).")
        self.click(self.link_menu_principal_seguridad, desc="Menú Seguridad Principal")

    def _obtener_paso_abrir_menu_seguridad(self) -> Callable[[], None]:
        self.log.debug("Encadenando: Abrir Seguridad.")
        return lambda: self.abrir_menu_seguridad()
