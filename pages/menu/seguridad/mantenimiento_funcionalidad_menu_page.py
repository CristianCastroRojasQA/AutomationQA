from playwright.sync_api import Page

from pages.menu.seguridad.menu_seguridad import MenuSeguridadPage


class MantenimientoFuncionalidadPage(MenuSeguridadPage):
    """
    Representa la sección 'Mantenimiento Funcionalidad' dentro del menú de Seguridad.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="Seguridad_Mantenimiento_Funcionalidad")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: (Sub-dropdown)
        self.link_menu_mantenimiento_funcionalidad = page.get_by_role("link", name="Mantenimiento de Funcionalidad", exact=True)
        self.log.debug(f"Locator 'sub_menu_mantenimiento_funcionalidad' inicializado.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def _obtener_pasos_para_mantenimiento_funcionalidad(self):
        return [
            self._obtener_paso_abrir_menu_seguridad(),
            lambda: self.hover(self.link_menu_mantenimiento_funcionalidad,
                               desc="Sub-menú Mantenimiento de Funcionalidad"),
        ]

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_mantenimiento_funcionalidad(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de Funcionalidad'."""
        self.log.info(f"Iniciando navegación a 'Mantenimiento de Funcionalidad' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_mantenimiento_funcionalidad() + [
            lambda: self.click(self.link_menu_mantenimiento_funcionalidad,
                               desc="Link Mantenimiento de Funcionalidad")
        ]
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="SECUC008",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Mantenimiento de Funcionalidad"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Seguridad_Mantenimiento_Funcionalidad",
        )
