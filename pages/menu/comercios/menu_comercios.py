from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import Callable


class MenuComerciosPage(BasePage):
    """
    Clase base para la página del menú principal de Comercios.
    Proporciona métodos para interactuar con el menú de nivel superior
    y una función genérica para la navegación a subpáginas.
    """

    def __init__(self, page: Page, logger_name: str = "MenuComercios"):
        super().__init__(page, logger_name=logger_name)
        # Locator para el menú principal de Comercios
        self.link_menu_principal_comercios = page.locator("#MERCHANT_KEY")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: (Sub-dropdown)
        self.sub_menu_consultar_comercio = page.locator("#AMUC008_MerchantSearch")
        self.log.debug("Locator 'sub_menu_consultar_comercio' inicializado.")

        self.sub_menu_alta_comercio = page.locator("#AMUC002_MerchantAdd")
        self.log.debug("Locator 'sub_menu_alta_comercio' inicializado.")

        self.sub_menu_mantenimiento_preafiliacion = page.locator("#AMDUC002_MerchantEntrySearch")
        self.log.debug("Locator 'sub_menu_mantenimiento_preafiliacion' inicializado.")

        self.sub_menu_alta_preafiliacion = page.locator("#AMDUC001_MerchantDataEntryAdd")
        self.log.debug("Locator 'sub_menu_alta_preafiliacion' inicializado.")

        self.sub_menu_consulta_transacciones = page.locator("#ATXUC012_AcquirerTransInfo")
        self.log.debug("Locator 'sub_menu_consulta_transacciones' inicializado.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def abrir_menu_comercios(self):
        """
        Hace click en el menú principal de Comercios para desplegar sus opciones.
        """
        self.click(self.link_menu_principal_comercios, desc="Menú Comercios")

    def _obtener_paso_abrir_menu_comercios(self) -> Callable[[], None]:
        """
        Retorna un callable para el paso de abrir el menú de configuración.
        Útil para construir secuencias de navegación.
        """
        return lambda: self.abrir_menu_comercios()

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_consultar_comercio_sucursal(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Consultar Comercio / Sucursal'."""
        self.log.info(
            f"Iniciando navegación a 'Consultar Comercio / Sucursal' para el caso: '{nombre_caso_prueba}'."
        )

        pasos = [
            self._obtener_paso_abrir_menu_comercios(),
            lambda: self.click(self.sub_menu_consultar_comercio, desc="Consultar Comercio / Sucursal"),
        ]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMUC008",
            locator_titulo_pagina=self.page.get_by_role("heading", name="Búsqueda de Comercios / Sucursales"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Comercios_Consultar_Comercio_Sucursal",
        )

    def navegar_a_alta_comercio(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta de Comercio'."""
        self.log.info(
            f"Iniciando navegación a 'Alta de Comercio' para el caso: '{nombre_caso_prueba}'."
        )

        pasos = [
            self._obtener_paso_abrir_menu_comercios(),
            lambda: self.click(self.sub_menu_alta_comercio, desc="Alta de Comercios"),
        ]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMUC002",
            locator_titulo_pagina=self.page.locator("span[id$='lblStepTtl1']"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Comercios_Alta_Comercio",
        )

    def navegar_a_mantenimiento_preafilicion_comercio(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento Preafilición Comercio'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento Preafilición Comercio' para el caso: '{nombre_caso_prueba}'."
        )

        pasos = [
            self._obtener_paso_abrir_menu_comercios(),
            lambda: self.click(self.sub_menu_mantenimiento_preafiliacion, desc="Mantenimiento Preafilición Comercio"),
        ]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMDUC002",
            locator_titulo_pagina=self.page.locator("span[id$='lbl_title']"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Mantenimiento Preafilición Comercio",
        )

    def navegar_a_alta_preafilicion_comercio(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta Preafilición Comercio'."""
        self.log.info(
            f"Iniciando navegación a 'Alta Preafilición Comercio' para el caso: '{nombre_caso_prueba}'."
        )

        pasos = [
            self._obtener_paso_abrir_menu_comercios(),
            lambda: self.click(self.sub_menu_alta_preafiliacion, desc="Alta Preafilición Comercio"),
        ]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMDUC001",
            locator_titulo_pagina=self.page.locator("span[id$='titlePageLabel']"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Alta Preafilición Comercio",
        )

    def navegar_a_consulta_transacciones(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Consulta de Transacciones'."""
        self.log.info(
            f"Iniciando navegación a 'Consulta de Transacciones' para el caso: '{nombre_caso_prueba}'."
        )

        pasos = [
            self._obtener_paso_abrir_menu_comercios(),
            lambda: self.click(self.sub_menu_consulta_transacciones, desc="Consulta de Transacciones"),
        ]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ATXUC012",
            locator_titulo_pagina=self.page.locator("span[id$='lblTitle']"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Consulta de Transacciones",
        )
