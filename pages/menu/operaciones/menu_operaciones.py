from typing import Callable

from playwright.sync_api import Page

from pages.base_page import BasePage


class MenuOperacionesPage(BasePage):
    """
    Clase base para la página del menú principal de Operaciones.
    Proporciona métodos para interactuar con el menú de nivel superior
    y una función genérica para la navegación a subpáginas.
    """

    def __init__(self, page: Page, logger_name: str = "MenuOperaciones"):
        super().__init__(page, logger_name=logger_name)
        # NIVEL 1: Menú Principal
        self.link_menu_principal_operaciones = page.get_by_role("link", name="Operaciones")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: Sub-menús
        self.sub_menu_consultar_debitos_automaticos = page.get_by_role("link", name="Consultar Débitos Automáticos")
        self.log.debug("Locator 'sub_menu_consultar_debitos_automaticos' inicializado.")

        self.sub_menu_mantenimiento_fee_collection = page.get_by_role("link",
                                                                      name="Mantenimiento Fee Collection Adquirente")
        self.log.debug("Locator 'sub_menu_mantenimiento_fee_collection' inicializado.")

        self.sub_menu_mantenimiento_pagos = page.get_by_role("link", name="Mantenimiento Pagos")
        self.log.debug("Locator 'sub_menu_mantenimiento_pagos' inicializado.")

        self.sub_menu_devolucion_manual = page.get_by_role("link", name="Devolución Manual")
        self.log.debug("Locator 'sub_menu_devolucion_manual' inicializado.")

        self.sub_menu_administracion_disputas_adquirente = page.get_by_role("link",
                                                                            name="Administración Disputas Adquirente")
        self.log.debug("Locator 'sub_menu_administracion_disputas_adquirente' inicializado.")

        self.sub_menu_devolucion_debitos_automaticos = page.get_by_role("link",
                                                                        name="Devolución Débitos Automáticos")
        self.log.debug("Locator 'sub_menu_devolucion_debitos_automaticos' inicializado.")

        self.sub_menu_cuadratura = page.get_by_role("link", name="Cuadratura")
        self.log.debug("Locator 'sub_menu_cuadratura' inicializado.")

        self.log.debug(f"Mapeando sub-menús de Operaciones. Total locators: {len(self.__dict__)}")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def abrir_menu_operaciones(self):
        """Hace click en el menú principal de Operaciones."""
        self.log.info("[NAV] Desplegando menú principal de: Operaciones (#OPERATIONS_KEY)")
        self.log.debug("Esperando que el menú de operaciones sea interactuable (Clickable).")
        self.click(self.link_menu_principal_operaciones, desc="Menú Configuración Principal")


    def _obtener_paso_abrir_menu_operaciones(self) -> Callable[[], None]:
        """Retorna un callable para el paso de abrir el menú de operaciones."""
        self.log.debug("Encadenando: Abrir Operaciones.")
        return lambda: self.abrir_menu_operaciones()

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_consultar_debitos_automaticos(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Consultar Débitos Automáticos'."""
        self.log.info(f"Iniciando navegación a 'Consultar Débitos Automáticos' para el caso: '{nombre_caso_prueba}'.")
        pasos = [
            self._obtener_paso_abrir_menu_operaciones(),
            lambda: self.click(self.sub_menu_consultar_debitos_automaticos, desc="Consultar Débitos Automáticos"),
        ]
        self.log.info(f"Destino: ACMUC033  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ACMUC033",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Consultar Débitos Automáticos"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Operaciones_Consultar_Debitos_Automaticos",
        )

    def navegar_a_mantenimiento_fee_collection(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento Fee Collection Adquirente'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento Fee Collection Adquirente' para el caso: '{nombre_caso_prueba}'.")
        pasos = [
            self._obtener_paso_abrir_menu_operaciones(),
            lambda: self.click(self.sub_menu_mantenimiento_fee_collection,
                               desc="Mantenimiento Fee Collection Adquirente"),
        ]
        self.log.info(f"Destino: ATXUC029  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ATXUC029",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Mantenimiento Fee Collection Adquirente"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Operaciones_Mantenimiento_Fee_Collection_Adquirente",
        )

    def navegar_a_mantenimiento_pagos(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento Pagos'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento Pagos' para el caso: '{nombre_caso_prueba}'.")
        pasos = [
            self._obtener_paso_abrir_menu_operaciones(),
            lambda: self.click(self.sub_menu_mantenimiento_pagos,
                               desc="Mantenimiento Pagos"),
        ]
        self.log.info(f"Destino: ACMUC013  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ACMUC013",
            locator_titulo_pagina=self.page.locator("h3").get_by_text("Mantenimiento Pagos"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Operaciones_Mantenimiento_Pagos",
        )

    def navegar_a_devolucion_manual(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Devolución Manual'."""
        self.log.info(
            f"Iniciando navegación a 'Devolución Manual' para el caso: '{nombre_caso_prueba}'.")
        pasos = [
            self._obtener_paso_abrir_menu_operaciones(),
            lambda: self.click(self.sub_menu_devolucion_manual,
                               desc="Devolución Manual"),
        ]
        self.log.info(f"Destino: ATXUC014  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ATXUC014",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Devolución Manual"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Operaciones_Devolución_Manual",
        )

    def navegar_a_administracion_disputas_adquirente(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Administración Disputas Adquirente'."""
        self.log.info(
            f"Iniciando navegación a 'Administración Disputas Adquirente' para el caso: '{nombre_caso_prueba}'.")
        pasos = [
            self._obtener_paso_abrir_menu_operaciones(),
            lambda: self.click(self.sub_menu_administracion_disputas_adquirente,
                               desc="Administración Disputas Adquirente"),
        ]
        self.log.info(f"Destino: GetControversy  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="GetControversy",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Administración Disputas Adquirente"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Operaciones_Administración_Disputas_Adquirente",
        )

    def navegar_a_devolucion_debitos_automaticos(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Devolución Débitos Automáticos'."""
        self.log.info(
            f"Iniciando navegación a 'Devolución Débitos Automáticos' para el caso: '{nombre_caso_prueba}'.")
        pasos = [
            self._obtener_paso_abrir_menu_operaciones(),
            lambda: self.click(self.sub_menu_devolucion_debitos_automaticos,
                               desc="Devolución Débitos Automáticos"),
        ]
        self.log.info(f"Destino: ACMUC036 Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ACMUC036",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Devolución Masiva Débitos Automáticos"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Operaciones_Devolución_Débitos_Automáticos",
        )

    def navegar_a_cuadratura(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Cuadratura'."""
        self.log.info(
            f"Iniciando navegación a 'Cuadratura' para el caso: '{nombre_caso_prueba}'.")
        pasos = [
            self._obtener_paso_abrir_menu_operaciones(),
            lambda: self.click(self.sub_menu_cuadratura,
                               desc="Cuadratura"),
        ]
        self.log.info(f"Destino: DailyQuadrature Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="DailyQuadrature",
            locator_titulo_pagina=self.page.locator("h3").get_by_text("Cuadratura"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Operaciones_Cuadratura",
        )
