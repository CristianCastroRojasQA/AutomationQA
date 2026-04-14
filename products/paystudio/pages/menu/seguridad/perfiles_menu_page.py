from playwright.sync_api import Page

from products.paystudio.pages.menu.seguridad.menu_seguridad import MenuSeguridadPage


class PerfilesMenuPage(MenuSeguridadPage):
    """
    Representa la sección 'Perfiles' dentro del menú de Seguridad.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="Seguridad_Perfiles")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: PERFILES (Sub-dropdown)
        self.sub_menu_perfiles = page.get_by_role("link", name="Perfiles")
        self.log.debug(f"Locator 'sub_menu_perfiles' inicializado.")

        # Sub-menus y enlaces directos de Perfiles
        self.link_perfiles_alta_perfil = page.get_by_role("link", name="Alta de Perfil")
        self.log.debug(f"Locator 'link_perfiles_alta_perfil' inicializado.")

        self.link_perfiles_mantenimiento_perfil = page.get_by_role("link", name="Mantenimiento de Perfil")
        self.log.debug(f"Locator 'link_perfiles_mantenimiento_perfil' inicializado.")

        self.link_perfiles_baja_perfil = page.get_by_role("link", name="Baja de Perfil")
        self.log.debug(f"Locator 'link_perfiles_baja_perfil' inicializado.")

        self.log.debug(f"Estructura Perfiles (RoleAdministration) mapeada. {len(self.__dict__)} enlaces detectados.")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def _obtener_pasos_para_perfiles(self):
        self.log.debug("Encadenando: Abrir Seguridad > Perfiles.")
        return [
            self._obtener_paso_abrir_menu_seguridad(),
            lambda: self.hover(self.sub_menu_perfiles, desc="Sub-menú Perfiles"),
        ]

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_perfiles_alta_perfil(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta de Perfil'."""
        self.log.info(f"Iniciando navegación a 'Alta de Perfil' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_perfiles() + [
            lambda: self.click(self.link_perfiles_alta_perfil,
                               desc="Link Alta de Perfil")
        ]
        self.log.info(f"Destino: RoleAdministration  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="RoleAdministration",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Seleccionar Perfil"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Usuarios_Alta_Perfil",
        )

    def navegar_a_perfiles_mantenimiento_perfil(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de Perfil'."""
        self.log.info(f"Iniciando navegación a 'Mantenimiento de Perfil' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_perfiles() + [
            lambda: self.click(self.link_perfiles_mantenimiento_perfil,
                               desc="Link Mantenimiento de Perfil")
        ]
        self.log.info(f"Destino: RoleAdministration  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="RoleAdministration",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Seleccionar Perfil"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Usuarios_Mantenimiento_Perfil",
        )

    def navegar_a_perfiles_baja_perfil(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Baja de Perfil'."""
        self.log.info(f"Iniciando navegación a 'Baja de Perfil' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_perfiles() + [
            lambda: self.click(self.link_perfiles_baja_perfil,
                               desc="Link Baja de Perfil")
        ]
        self.log.info(f"Destino: RoleAdministration  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="RoleAdministration",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Seleccionar Perfil"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Usuarios_Baja_Perfil",
        )
