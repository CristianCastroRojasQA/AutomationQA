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
    URL_TIMEOUT = 15000
    TITLE_TIMEOUT = 10000
    ANIMATION_WAIT = 500

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

    def _navegar_a_pagina_estandar(
            self,
            pasos_de_navegacion: List[Callable[[], None]],
            segmento_url_esperado: str,
            locator_titulo_pagina: Locator,
            nombre_caso_prueba: str,
            etiqueta_evidencia: str
    ) -> str:
        """
        Ejecuta una secuencia de pasos para navegar a una página, espera su carga,
        captura una evidencia y retorna la URL actual.

        Args:
            pasos_de_navegacion: Lista de funciones callable que representan los pasos
                                 necesarios para llegar al enlace final (clicks, hovers).
            segmento_url_esperado: Segmento de la URL esperado para verificar la navegación.
            locator_titulo_pagina: Locator del elemento que contiene el título de la página.
            nombre_caso_prueba: Nombre del caso de prueba para la evidencia y logs.
            etiqueta_evidencia: Etiqueta descriptiva para el nombre del archivo de evidencia.

        Returns:
            La URL actual de la página después de la navegación.
        """
        for paso in pasos_de_navegacion:
            paso()

        self.page.wait_for_url(f"**/{segmento_url_esperado}*", timeout=self.URL_TIMEOUT)
        self.page.wait_for_load_state("networkidle")

        locator_titulo_pagina.wait_for(state="visible", timeout=self.TITLE_TIMEOUT)
        self.page.wait_for_timeout(self.ANIMATION_WAIT)

        capturar_evidencia(self.page, nombre_caso_prueba, f"Pantalla_{etiqueta_evidencia}")
        self.log.info(f"Navegación exitosa a {segmento_url_esperado}")
        return self.page.url
