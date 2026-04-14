from playwright.sync_api import Page
from products.paystudio.pages.base_page import BasePage
from typing import Callable


class MenuComerciosPage(BasePage):
    """
    Clase base para la página del menú principal de Comercios.
    Proporciona métodos para interactuar con el menú de nivel superior
    y una función genérica para la navegación a subpáginas.
    """

    def __init__(self, page: Page, logger_name: str = "MenuComercios"):
        super().__init__(page, logger_name=logger_name)

        # NIVEL 1: Locator para el menú principal de Comercios
        self.link_menu_principal_comercios = page.get_by_role("link", name="Comercios")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: Sub-menús
        self.sub_menu_consultar_comercio = page.get_by_role("link", name="Consultar Comercio / Sucursal")
        self.log.debug("Locator 'sub_menu_consultar_comercio' inicializado.")

        self.sub_menu_alta_comercio = page.get_by_role("link", name="Alta de Comercio")
        self.log.debug("Locator 'sub_menu_alta_comercio' inicializado.")

        self.sub_menu_mantenimiento_preafiliacion = page.get_by_role("link",
                                                                     name="Mantenimiento Preafiliación Comercio")
        self.log.debug("Locator 'sub_menu_mantenimiento_preafiliacion' inicializado.")

        self.sub_menu_alta_preafiliacion = page.get_by_role("link", name="Alta Preafiliación Comercio")
        self.log.debug("Locator 'sub_menu_alta_preafiliacion' inicializado.")

        self.sub_menu_consulta_transacciones = page.get_by_role("link", name="Consulta de Transacciones")
        self.log.debug("Locator 'sub_menu_consulta_transacciones' inicializado.")

        self.log.debug(f"Mapeando sub-menús de Comercios. Total locators: {len(self.__dict__)}")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")
        # ------------------------------------------------------------------
        # Pasos reutilizables para construir secuencias de navegación
        # ------------------------------------------------------------------

    def abrir_menu_comercios(self):
        """Hace click en el menú principal de Comercios."""
        self.log.info("[NAV] Desplegando menú principal de Comercios (#MERCHANT_KEY)")
        self.log.debug("Esperando que el menú de comercios sea interactuable (Clickable).")
        self.click(self.link_menu_principal_comercios, desc="Menú Comercios")

    def _obtener_paso_abrir_menu_comercios(self) -> Callable[[], None]:
        """Retorna un callable para el paso de abrir el menú de comercios."""
        self.log.debug("Encadenando: Abrir Comercios.")
        return lambda: self.abrir_menu_comercios()

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_consultar_comercio_sucursal(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Consultar Comercio / Sucursal'."""
        self.log.info(f"Iniciando navegación a 'Consultar Comercio / Sucursal' para el caso: '{nombre_caso_prueba}'.")

        pasos = [
            self._obtener_paso_abrir_menu_comercios(),
            lambda: self.click(self.sub_menu_consultar_comercio, desc="Consultar Comercio / Sucursal"),
        ]
        self.log.info(f"Destino: AMUC008  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMUC008",
            # Cambiado de heading genérico a texto exacto para evitar fallos de Timeout
            locator_titulo_pagina=self.page.get_by_text("Búsqueda de Comercios / Sucursales"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Comercios_Consultar_Comercio_Sucursal",
        )

    def navegar_a_alta_comercio(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta de Comercio'."""
        self.log.info(f"Iniciando navegación a 'Alta de Comercio' para el caso: '{nombre_caso_prueba}'.")
        pasos = [
            self._obtener_paso_abrir_menu_comercios(),
            lambda: self.click(self.sub_menu_alta_comercio, desc="Alta de Comercios"),
        ]
        self.log.info(f"Destino: AMUC002  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        self.log.info("Accediendo al Wizard de Alta (AMUC002). Validando Paso 1.")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMUC002",
            locator_titulo_pagina=self.page.get_by_text("Información Básica (Paso 1 de 12)"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Comercios_Alta_Comercio",
        )

    def navegar_a_mantenimiento_preafilicion_comercio(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento Preafiliación Comercio'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento Preafiliación Comercio' para el caso: '{nombre_caso_prueba}'.")

        pasos = [
            self._obtener_paso_abrir_menu_comercios(),
            lambda: self.click(self.sub_menu_mantenimiento_preafiliacion, desc="Mantenimiento Preafiliación Comercio"),
        ]
        self.log.info(f"Destino: AMDUC002  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMDUC002",
            locator_titulo_pagina=self.page.get_by_text("Búsqueda Preafiliación"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Comercios_Mantenimiento_Preafiliacion",
        )

    def navegar_a_alta_preafilicion_comercio(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta Preafiliación Comercio'."""
        self.log.info(f"Iniciando navegación a 'Alta Preafiliación Comercio' para el caso: '{nombre_caso_prueba}'.")

        pasos = [
            self._obtener_paso_abrir_menu_comercios(),
            lambda: self.click(self.sub_menu_alta_preafiliacion, desc="Alta Preafiliación Comercio"),
        ]
        self.log.info(f"Destino: AMDUC001  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMDUC001",
            locator_titulo_pagina=self.page.get_by_text("Alta Preafiliación de Comercio"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Comercios_Alta_Preafiliacion",
        )

    def navegar_a_consulta_transacciones(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Consulta de Transacciones'."""
        self.log.info(f"Iniciando navegación a 'Consulta de Transacciones' para el caso: '{nombre_caso_prueba}'.")
        self.log.warning(
            "Navegando a Consulta de Transacciones. "
            "Este módulo suele requerir tiempos de carga mayores."
        )
        pasos = [
            self._obtener_paso_abrir_menu_comercios(),
            lambda: self.click(self.sub_menu_consulta_transacciones, desc="Consulta de Transacciones"),
        ]
        self.log.info(f"Destino: ATXUC012  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ATXUC012",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Consulta de Transacciones", exact=True),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Comercios_Consulta_Transacciones",
        )
