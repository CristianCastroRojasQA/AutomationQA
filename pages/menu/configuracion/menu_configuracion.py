from playwright.sync_api import Page
from pages.base_page import BasePage
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

    def abrir_menu_configuracion(self):
        self.click(self.link_menu_principal_configuracion, desc="Menú Configuración Principal")

    def _obtener_paso_abrir_menu_configuracion(self) -> Callable[[], None]:
        return lambda: self.abrir_menu_configuracion()
