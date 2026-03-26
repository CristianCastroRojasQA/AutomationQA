from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from typing import Callable, List
from utils.screenshots import capturar_evidencia


class MenuConfiguracionPage(BasePage):
    """
    Clase base para la página del menú principal de Configuración.
    Proporciona métodos para interactuar con el menú de nivel superior
    y una función genérica para la navegación a subpáginas.
    """

    def __init__(self, page: Page, logger_name: str = "MenuConfiguracion"):
        super().__init__(page, logger_name=logger_name)
        # Locator para el menú principal de Configuración
        self.link_menu_principal_configuracion = page.locator("#CONFIGURATION_KEY")

    def abrir_menu_configuracion(self):
        """
        Hace click en el menú principal de Configuración para desplegar sus opciones.
        """
        self.click(self.link_menu_principal_configuracion, desc="Menú Configuración Principal")

    def _obtener_paso_abrir_menu_configuracion(self) -> Callable[[], None]:
        """
        Retorna un callable para el paso de abrir el menú de configuración.
        Útil para construir secuencias de navegación.
        """
        return lambda: self.abrir_menu_configuracion()
