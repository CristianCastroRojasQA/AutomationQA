from playwright.sync_api import Page
from pages.menu.configuracion.menu_configuracion import MenuConfiguracionPage


class GestionListasMenuPage(MenuConfiguracionPage):
    """
    Representa la sección 'Gestión de Listas de Autorización' dentro de Configuración.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="ConfiguracionGestionListas")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: GESTIÓN DE LISTAS DE AUTORIZACIÓN
        self.sub_menu_gestion_listas = page.get_by_role("link", name="Gestión de Listas de Autorización")
        self.log.debug(f"Locator 'sub_menu_gestion_listas_autorizacion' inicializado.")

        # NIVEL 3: DENTRO DE GESTIÓN DE LISTAS
        self.link_alta_lista = page.get_by_role("link", name="Alta de lista para reglas de autorización")
        self.log.debug(f"Locator 'link_gestion_alta_lista_reglas_autorizacion' inicializado.")
        self.link_mantenimiento_lista = page.get_by_role("link",
                                                         name="Mantenimiento de lista para reglas de autorización")
        self.log.debug(f"Locator 'link_gestion_mantenimiento_lista_reglas_autorizacion' inicializado.")
        self.link_mantenimiento_valores = page.get_by_role("link",
                                                           name="Mantenimiento de valores de lista para reglas de autorización")
        self.log.debug(f"Locator 'link_gestion_mantenimiento_valores_lista_reglas_autorizacion' inicializado.")
        self.link_eliminar_lista = page.get_by_role("link", name="Eliminar lista para reglas de autorizacion")
        self.log.debug(f"Locator 'link_gestion_eliminar_lista_reglas_autorizacion' inicializado.")

        self.log.debug(
            f"Estructura Gestión de Listas (AuthorizationRuleListAdministration) mapeada. {len(self.__dict__)} enlaces detectados.")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    def _obtener_pasos_para_gestion_listas_autorizacion(self):
        self.log.debug("Encadenando: Abrir Configuración > Gestión de Listas de Autorización.")
        return [
            self._obtener_paso_abrir_menu_configuracion(),
            lambda: self.hover(self.sub_menu_gestion_listas,
                               desc="Sub-menú Gestión de Listas de Autorización"),
        ]

    def navegar_a_gestion_alta_lista_reglas_autorizacion(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta de lista para reglas de autorización'."""
        self.log.info(
            f"Iniciando navegación a 'Alta de lista para reglas de autorización' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_alta_lista,
                               desc="Link Alta Lista para Reglas de Autorización"),
        ]
        self.log.info(
            f"Destino: AddAuthorizationRuleList  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AddAuthorizationRuleList",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Añadir Lista de Reglas de Autorización"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="GestionListas_Alta_Lista_Reglas_Autorizacion"
        )

    def navegar_a_gestion_mantenimiento_lista_reglas_autorizacion(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de lista para reglas de autorización'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento de lista para reglas de autorización' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_mantenimiento_lista,
                               desc="Link Mantenimiento de Lista para Reglas de Autorización"),
        ]
        self.log.info(
            f"Destino: UpdateAuthorizationRuleListSearch  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="UpdateAuthorizationRuleListSearch",
            locator_titulo_pagina=self.page.locator("span").get_by_text(
                "Selecciona una Lista de Reglas de Autorización"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="GestionListas_Mantenimiento_Lista_Reglas_Autorizacion"
        )

    def navegar_a_gestion_mantenimiento_valores_lista_reglas_autorizacion(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de valores de lista para reglas de autorización'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento de valores de lista para reglas de autorización' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_mantenimiento_valores,
                               desc="Link Mantenimiento de Valores de Lista para Reglas de Autorización")
        ]
        self.log.info(
            f"Destino: UpdateAuthorizationRuleListValuesSearch  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="UpdateAuthorizationRuleListValuesSearch",
            locator_titulo_pagina=self.page.locator("span").get_by_text(
                "Selecciona una Lista de Reglas de Autorización"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="GestionListas_Mantenimiento_Valores_Lista_Reglas_Autorizacion"
        )

    def navegar_a_gestion_eliminar_listas_reglas_autorizacion(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Eliminar lista para reglas de autorización'."""
        self.log.info(
            f"Iniciando navegación a 'Eliminar lista para reglas de autorización' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_eliminar_lista,
                               desc="Link Eliminar Lista para Reglas de Autorización")
        ]
        self.log.info(
            f"Destino: DeleteAuthorizationRuleList  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="DeleteAuthorizationRuleList",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Eliminar Lista de Reglas de Autorización"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="GestionListas_Eliminar_Lista_Reglas_Autorizacion"
        )
