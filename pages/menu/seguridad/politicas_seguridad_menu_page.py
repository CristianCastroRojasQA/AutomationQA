from playwright.sync_api import Page

from pages.menu.seguridad.menu_seguridad import MenuSeguridadPage


class PoliticasSeguridadPage(MenuSeguridadPage):
    """
    Representa la sección 'Configuración Políticas Seguridad' dentro del menú de Seguridad.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="Seguridad_Politicas_Seguridad")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: (Sub-dropdown)
        self.link_menu_politicas_seguridad = page.get_by_role("link", name="Configuración Políticas Seguridad")
        self.log.debug(f"Locator 'sub_menu_politicas_seguridad' inicializado.")

        self.log.debug(
            f"Estructura Configuración Politicas de Seguridad (SecurityPolicyConfiguration) mapeada. {len(self.__dict__)} enlaces detectados.")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def _obtener_pasos_para_politicas_seguridad(self):
        self.log.debug("Encadenando: Abrir Seguridad > Configuración Politicas de Seguridad.")
        return [
            self._obtener_paso_abrir_menu_seguridad(),
            lambda: self.hover(self.link_menu_politicas_seguridad,
                               desc="Sub-menú Configuración Políticas Seguridad"),
        ]

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_configuracion_politicas_seguridad(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Configuración Políticas Seguridad."""
        self.log.info(
            f"Iniciando navegación a 'Configuración Políticas Seguridad' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_politicas_seguridad() + [
            lambda: self.click(self.link_menu_politicas_seguridad,
                               desc="Link Configuración Políticas Seguridad")
        ]
        self.log.info(f"Destino: SECUC002  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="SECUC002",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Configuración Políticas de Seguridad"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Seguridad_Configuracion_Politicas_Seguridad",
        )
