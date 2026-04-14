from playwright.sync_api import Page
from products.paystudio.pages.base_page import BasePage
from typing import Callable


class MenuConfiguracionPage(BasePage):
    """
    Clase base para la página del menú principal de Configuración.
    Proporciona métodos para interactuar con el menú de nivel superior
    y una función genérica para la navegación a subpáginas.
    """

    def __init__(self, page: Page, logger_name: str = "MenuConfiguracion"):
        super().__init__(page, logger_name=logger_name)
        # Nivel 1: Menú Principal
        self.link_menu_principal_configuracion = page.get_by_role("link", name="Configuración")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

    def abrir_menu_configuracion(self):
        self.log.info("[NAV] Desplegando menú principal de Configuración (#CONFIGURATION_KEY)")
        self.log.debug("Esperando que el menú de Configuración sea interactuable (Clickable).")
        self.click(self.link_menu_principal_configuracion, desc="Menú Configuración Principal")

    def _obtener_paso_abrir_menu_configuracion(self) -> Callable[[], None]:
        self.log.debug("Encadenando: Abrir Configuración.")
        return lambda: self.abrir_menu_configuracion()
