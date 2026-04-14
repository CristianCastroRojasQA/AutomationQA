from playwright.sync_api import Page

from pages.menu.seguridad.menu_seguridad import MenuSeguridadPage


class ReportesMenuPage(MenuSeguridadPage):
    """
    Representa la sección 'Reportes' dentro del menú de Seguridad.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="Seguridad_Reportes")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: REPORTES (Sub-dropdown)
        self.sub_menu_reportes = page.get_by_role("link", name="Reportes")
        self.log.debug(f"Locator 'sub_menu_reportes' inicializado.")

        # Sub-menus y enlaces directos de Perfiles
        self.link_reportes_usuarios_accesos = page.get_by_role("link", name="Reporte de Usuarios y Accesos")
        self.log.debug(f"Locator 'link_reportes_usuarios_accesos' inicializado.")

        self.link_reportes_perfiles = page.get_by_role("link", name="Reporte de Perfiles")
        self.log.debug(f"Locator 'link_reportes_perfiles' inicializado.")

        self.link_reportes_intentos_accesos = page.get_by_role("link", name="Reporte Intento de Accesos")
        self.log.debug(f"Locator 'link_reportes_intentos_accesos' inicializado.")

        self.log.debug(f"Estructura Reportes (SecurityReports) mapeada. {len(self.__dict__)} enlaces detectados.")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def _obtener_pasos_para_reportes(self):
        self.log.debug("Encadenando: Abrir Seguridad > Reportes.")
        return [
            self._obtener_paso_abrir_menu_seguridad(),
            lambda: self.hover(self.sub_menu_reportes, desc="Sub-menú Reportes"),
        ]

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_reportes_usuarios_accesos(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Reporte de Usuarios y Accesos'."""
        self.log.info(f"Iniciando navegación a 'Reporte de Usuarios y Accesos' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_reportes() + [
            lambda: self.click(self.link_reportes_usuarios_accesos,
                               desc="Link Reporte de Usuarios y Accesos")
        ]
        self.log.info(f"Destino: SERUC001  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="SERUC001",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Reporte de Usuarios y Accesos"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Reportes_Reporte_Usuarios_Accesos",
        )

    def navegar_a_reportes_perfiles(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Reporte de Perfiles'."""
        self.log.info(f"Iniciando navegación a 'Reporte de Perfiles' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_reportes() + [
            lambda: self.click(self.link_reportes_perfiles,
                               desc="Link Reporte de Perfiles")
        ]
        self.log.info(f"Destino: SERUC002  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="SERUC002",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Reporte de Perfiles"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Reportes_Reporte_Perfiles",
        )

    def navegar_a_reportes_intentos_acceso(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Reporte Intento de Accesos'."""
        self.log.info(f"Iniciando navegación a 'Reporte Intento de Accesos' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_reportes() + [
            lambda: self.click(self.link_reportes_intentos_accesos,
                               desc="Reporte Intento de Accesos")
        ]
        self.log.info(f"Destino: SERUC003  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="SERUC003",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Reporte de Intento de Accesos"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Reportes_Reporte_Intentos_Accesos",
        )
