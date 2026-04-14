from playwright.sync_api import Page

from pages.menu.seguridad.menu_seguridad import MenuSeguridadPage


class LogAuditoriaPage(MenuSeguridadPage):
    """
    Representa la sección 'Log de Auditoría' dentro del menú de Seguridad.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="Seguridad_Log_Auditoría")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: (Sub-dropdown)
        self.link_menu_log_auditoria = page.get_by_role("link", name="Log de Auditoría")
        self.log.debug(f"Locator 'sub_menu_log_auditoria' inicializado.")

        self.log.debug(f"Estructura Log de Auditoría (AUDUC001) mapeada. {len(self.__dict__)} enlaces detectados.")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def _obtener_pasos_para_log_auditoria(self):
        self.log.debug("Encadenando: Abrir Seguridad > Log de Auditoría.")
        return [
            self._obtener_paso_abrir_menu_seguridad(),
            lambda: self.hover(self.link_menu_log_auditoria,
                               desc="Sub-menú Log de Auditoría"),
        ]

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_log_audtoria(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Log de Auditoría."""
        self.log.info(
            f"Iniciando navegación a 'Log de Auditoría' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_log_auditoria() + [
            lambda: self.click(self.link_menu_log_auditoria,
                               desc="Link Log de Auditoría")
        ]
        self.log.info(f"Destino: AUDUC001  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AUDUC001",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Consulta Log Auditoría"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Seguridad_Log_Auditoría",
        )
