from playwright.sync_api import Page
from pages.menu.configuracion.menu_configuracion import MenuConfiguracionPage


class GestionListasMenuPage(MenuConfiguracionPage):
    """
    Representa la sección 'Gestión de Listas de Autorización' dentro del menú de Configuración.
    Contiene locators y métodos para interactuar con los enlaces relacionados.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="ConfiguracionGestionListas")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: GESTIÓN DE LISTAS DE AUTORIZACIÓN
        self.sub_menu_gestion_listas_autorizacion = page.locator("#AUTHORIZATION_RULE_LIST_KEY")
        self.log.debug(f"Locator 'sub_menu_gestion_listas_autorizacion' inicializado.")

        # NIVEL 3: DENTRO DE GESTIÓN DE LISTAS
        self.link_gestion_alta_lista_reglas_autorizacion = page.locator("#MIUC001_AddAuthRuleList")
        self.log.debug(f"Locator 'link_gestion_alta_lista_reglas_autorizacion' inicializado.")
        self.link_gestion_mantenimiento_lista_reglas_autorizacion = page.locator("#MIUC002_UpdateAuthListSearch")
        self.log.debug(f"Locator 'link_gestion_mantenimiento_lista_reglas_autorizacion' inicializado.")
        self.link_gestion_mantenimiento_valores_lista_reglas_autorizacion = page.locator(
            "#MIUC003_UpdtAuthListValSearch")
        self.log.debug(f"Locator 'link_gestion_mantenimiento_valores_lista_reglas_autorizacion' inicializado.")
        self.link_gestion_eliminar_lista_reglas_autorizacion = page.locator("#MIUC004_DeleteAuthList")
        self.log.debug(f"Locator 'link_gestion_eliminar_lista_reglas_autorizacion' inicializado.")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    def _obtener_pasos_para_gestion_listas_autorizacion(self):
        """
        Retorna la secuencia de pasos para abrir el menú principal de Configuración
        y hacer hover sobre el sub-menú 'Gestión de Listas de Autorización'.
        """
        self.log.debug("Obteniendo pasos para navegar al sub-menú 'Gestión de Listas de Autorización'.")
        return [
            self._obtener_paso_abrir_menu_configuracion(),
            lambda: self.hover(self.sub_menu_gestion_listas_autorizacion,
                               desc="Sub-menú Gestión de Listas de Autorización"),
        ]

    def navegar_a_gestion_alta_lista_reglas_autorizacion(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta de lista para reglas de autorización'."""
        self.log.info(
            f"Iniciando navegación a 'Alta de lista para reglas de autorización' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_gestion_alta_lista_reglas_autorizacion,
                               desc="Link Alta Lista para Reglas de Autorización"),
        ]
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AddAuthorizationRuleList",
            locator_titulo_pagina=self.page.get_by_text("Añadir Lista de Reglas de Autorización", exact=True),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="GestionListas_Alta_Lista_Reglas_Autorizacion"
        )

    def navegar_a_gestion_mantenimiento_lista_reglas_autorizacion(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de lista para reglas de autorización'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento de lista para reglas de autorización' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_gestion_mantenimiento_lista_reglas_autorizacion,
                               desc="Link Mantenimiento de Lista para Reglas de Autorización"),
        ]
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="UpdateAuthorizationRuleListSearch",
            locator_titulo_pagina=self.page.locator("span[id$='titlePageLabel2']"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="GestionListas_Mantenimiento_Lista_Reglas_Autorizacion"
        )

    def navegar_a_gestion_mantenimiento_valores_lista_reglas_autorizacion(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de valores de lista para reglas de autorización'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento de valores de lista para reglas de autorización' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_gestion_mantenimiento_valores_lista_reglas_autorizacion,
                               desc="Link Mantenimiento de Valores de Lista para Reglas de Autorización")
        ]
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="UpdateAuthorizationRuleListValuesSearch",
            locator_titulo_pagina=self.page.locator("span[id$='titlePageLabel2']"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="GestionListas_Mantenimiento_Valores_Lista_Reglas_Autorizacion"
        )

    def navegar_a_gestion_eliminar_listas_reglas_autorizacion(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Eliminar lista para reglas de autorización'."""
        self.log.info(
            f"Iniciando navegación a 'Eliminar lista para reglas de autorización' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_gestion_eliminar_lista_reglas_autorizacion,
                               desc="Link Eliminar Lista para Reglas de Autorización")
        ]
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="DeleteAuthorizationRuleList",
            locator_titulo_pagina=self.page.locator("span[id$='titlePageLabel2']"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="GestionListas_Eliminar_Lista_Reglas_Autorizacion"
        )
