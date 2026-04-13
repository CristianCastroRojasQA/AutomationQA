from playwright.sync_api import Page

from pages.menu.seguridad.menu_seguridad import MenuSeguridadPage


class ValidacionControlesMenuPage(MenuSeguridadPage):
    """
    Representa la sección 'Validación de Controles' dentro del menú de Seguridad.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="Seguridad_Validacion_Controles")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: VALIDACION CONTROLES (Sub-dropdown)
        self.sub_menu_validacion_controles = page.get_by_role("link", name="Validación de Controles")
        self.log.debug(f"Locator 'sub_menu_validacion_controles' inicializado.")

        # NIVEL 3: Sub-menus y enlaces directos de Mantenimiento de Niveles
        self.link_mantenimiento_niveles = page.get_by_role("link", name="Mantenimiento de Niveles")
        self.log.debug(f"Locator 'link_mantenimiento_niveles' inicializado.")

        self.link_alta_nivel = page.get_by_role("link", name="Alta de Nivel")
        self.log.debug(f"Locator 'sub_menu_alta_nivel' inicializado.")

        self.link_mantenimiento_nivel = page.get_by_role("link", name="Mantenimiento de Nivel", exact=True)
        self.log.debug(f"Locator 'sub_menu_mantenimiento_nivel' inicializado.")

        self.link_baja_nivel = page.get_by_role("link", name="Baja de Nivel")
        self.log.debug(f"Locator 'sub_menu_baja_nivel' inicializado.")

        self.log.debug(
            f"Estructura Validacion de Controles (LevelControlMainteinance) mapeada. {len(self.__dict__)} enlaces detectados.")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def _obtener_pasos_para_validacion(self):
        self.log.debug("Encadenando: Abrir Seguridad > Validación de Controles.")
        return [
            self._obtener_paso_abrir_menu_seguridad(),
            lambda: self.hover(self.sub_menu_validacion_controles, desc="Sub-menú Validación Controles"),
        ]

    def _obtener_pasos_para_validacion_controles(self):
        self.log.debug("Encadenando: Abrir Seguridad > Validación de Controles > Mantenimiento de Niveles.")
        return self._obtener_pasos_para_validacion() + [
            lambda: self.hover(self.link_mantenimiento_niveles, desc="Sub-menú Mantenimiento de Nivel"),
        ]

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_validacion_controles_alta_perfil(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta de Nivel'."""
        self.log.info(f"Iniciando navegación a 'Alta de Nivel' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_validacion_controles() + [
            lambda: self.click(self.link_alta_nivel,
                               desc="Link Alta de Nivel")
        ]
        self.log.info(f"Destino: SERUC009  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="SECUC009",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Alta de Nivel"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Validacion_Controles_Alta_de_Nivel",
        )

    def navegar_a_validacion_controles_mantenimiento_perfil(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de Nivel'."""
        self.log.info(f"Iniciando navegación a 'Mantenimiento de Nivel' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_validacion_controles() + [
            lambda: self.click(self.link_mantenimiento_nivel,
                               desc="Link Mantenimiento de Nivel")
        ]
        self.log.info(f"Destino: SERUC009  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="SECUC009",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Modificar Nivel"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Validacion_Controles_Mantenimiento_de_Nivel",
        )

    def navegar_a_validacion_controles_baja_perfil(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Baja de Nivel'."""
        self.log.info(f"Iniciando navegación a 'Baja de Nivel' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_validacion_controles() + [
            lambda: self.click(self.link_baja_nivel,
                               desc="Link Baja de Nivel")
        ]
        self.log.info(f"Destino: SERUC009  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="SECUC009",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Eliminar Nivel"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Validacion_Controles_Baja_de_Nivel",
        )
