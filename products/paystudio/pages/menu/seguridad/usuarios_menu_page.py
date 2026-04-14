from playwright.sync_api import Page

from products.paystudio.pages.menu.seguridad.menu_seguridad import MenuSeguridadPage


class UsuariosMenuPage(MenuSeguridadPage):
    """
    Representa la sección 'Usuarios' dentro del menú de Seguridad.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="Seguridad_Usuarios")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: USUARIOS (Sub-dropdown)
        self.sub_menu_usuarios = page.get_by_role("link", name="Usuarios")
        self.log.debug(f"Locator 'sub_menu_usuarios' inicializado.")

        # Sub-menus y enlaces directos de Usuarios
        self.link_usuario_mantenimiento_usuario = page.get_by_role("link", name="Mantenimiento de Usuario")
        self.log.debug(f"Locator 'link_usuario_mantenimiento_usuario' inicializado.")

        self.link_usuario_alta_usuario = page.get_by_role("link", name="Alta de Usuario")
        self.log.debug(f"Locator 'link_usuario_alta_usuario' inicializado.")

        self.link_usuario_habilitar_usuario_portal = page.get_by_role("link", name="Habilitar Usuario Portal Comercio")
        self.log.debug(f"Locator 'link_usuario_habilitar_usuario_portal' inicializado.")

        self.link_usuario_baja_usuario = page.get_by_role("link", name="Baja de Usuario")
        self.log.debug(f"Locator 'link_usuario_baja_usuario' inicializado.")

        self.log.debug(f"Estructura Usuarios (UserAdministration) mapeada. {len(self.__dict__)} enlaces detectados.")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def _obtener_pasos_para_usuarios(self):
        self.log.debug("Encadenando: Abrir Seguridad > Usuarios.")
        return [
            self._obtener_paso_abrir_menu_seguridad(),
            lambda: self.hover(self.sub_menu_usuarios, desc="Sub-menú Usuarios"),
        ]

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_usuario_mantenimiento_usuarios(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de Usuario'."""
        self.log.info(f"Iniciando navegación a 'Mantenimiento de Usuario' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_usuarios() + [
            lambda: self.click(self.link_usuario_mantenimiento_usuario,
                               desc="Link Mantenimiento de Usuario")
        ]
        self.log.info(f"Destino: P14CU7101_02Page  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="P14CU7101_02Page",
            locator_titulo_pagina=self.page.locator("h3").get_by_text("Búsqueda de Usuario"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Usuarios_Mantenimiento_Usuario",
        )

    def navegar_a_usuario_alta_usuario(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta de Usuario'."""
        self.log.info(f"Iniciando navegación a 'Alta de Usuario' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_usuarios() + [
            lambda: self.click(self.link_usuario_alta_usuario,
                               desc="Link Alta de Usuario")
        ]
        self.log.info(f"Destino: P14CU7101_02Page  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="P14CU7101_02Page",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Información del Usuario"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Usuarios_Alta_Usuario",
        )

    def navegar_a_usuario_habilitar_usuario_portal(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Habilitar Usuario Portal Comercio'."""
        self.log.info(
            f"Iniciando navegación a 'Habilitar Usuario Portal Comercio' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_usuarios() + [
            lambda: self.click(self.link_usuario_habilitar_usuario_portal,
                               desc="Link Habilitar Usuario Portal Comercio")
        ]
        self.log.info(f"Destino: EnablePortalUser  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="EnablePortalUser",
            locator_titulo_pagina=self.page.locator("h3").get_by_text(
                "Habilitar Usuario Administrador Portal Comercio"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Usuarios_Habilitar_Usuario_Portal_Comercio",
        )

    def navegar_a_usuario_baja_usuario(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Baja de Usuario'."""
        self.log.info(f"Iniciando navegación a 'Baja de Usuario' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_usuarios() + [
            lambda: self.click(self.link_usuario_baja_usuario,
                               desc="Link Baja de Usuario")
        ]
        self.log.info(f"Destino: UnsubscribePortalUser  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="UnsubscribePortalUser",
            locator_titulo_pagina=self.page.locator("h3").get_by_text("Baja de Usuario"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Usuarios_Baja_Usuario",
        )
