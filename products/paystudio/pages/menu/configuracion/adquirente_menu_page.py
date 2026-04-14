from playwright.sync_api import Page
from products.paystudio.pages.menu.configuracion.menu_configuracion import MenuConfiguracionPage


class AdquirenteMenuPage(MenuConfiguracionPage):
    """
    Representa la sección 'Adquirente' dentro del menú de Configuración.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="ConfiguracionAdquirente")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")

        # NIVEL 2: ADQUIRENTE (Sub-dropdown)
        self.sub_menu_adquirente = page.get_by_role("link", name="Adquirente")
        self.log.debug(f"Locator 'sub_menu_adquirente' inicializado.")

        # NIVEL 3: Sub-menus y enlaces directos de Adquirente
        self.link_adquirente_marcas_y_modelos_terminales = page.get_by_role("link",
                                                                            name="Marcas y Modelos de Terminales",
                                                                            exact=True)
        self.log.debug(f"Locator 'link_adquirente_marcas_y_modelos_terminales' inicializado.")

        # Sub-menú Terminales
        self.sub_menu_terminales = page.get_by_role("link", name="Terminales", exact=True)
        self.log.debug(f"Locator 'sub_menu_terminales' inicializado.")
        self.link_terminales_alta_terminal = page.get_by_role("link", name="Alta de Terminal")
        self.log.debug(f"Locator 'link_terminales_alta_terminal' inicializado.")
        self.link_terminales_mantenimiento_terminales = page.get_by_role("link", name="Mantenimiento de Terminales")
        self.log.debug(f"Locator 'link_terminales_mantenimiento_terminales' inicializado.")
        self.link_terminales_alta_masiva_terminales = page.get_by_role("link", name="Alta Masiva de Terminales")
        self.log.debug(f"Locator 'link_terminales_alta_masiva_terminales' inicializado.")
        self.link_terminales_consulta_stock_terminales = page.get_by_role("link", name="Consulta Stock de Terminales")
        self.log.debug(f"Locator 'link_terminales_consulta_stock_terminales' inicializado.")

        # Sub-menú Producto
        self.sub_menu_producto = page.get_by_role("link", name="Producto")
        self.log.debug(f"Locator 'sub_menu_producto' inicializado.")
        self.link_producto_alta_producto = page.get_by_role("link", name="Alta de Producto")
        self.log.debug(f"Locator 'link_producto_alta_producto' inicializado.")
        self.link_producto_mantenimiento_producto = page.get_by_role("link", name="Mantenimiento de Producto")
        self.log.debug(f"Locator 'link_producto_mantenimiento_producto' inicializado.")

        # Enlaces directos en Adquirente
        self.link_adquirente_mantenimiento_calendario = page.get_by_role("link",
                                                                         name="Mantenimiento Calendario Adquirente")
        self.log.debug(f"Locator 'link_adquirente_mantenimiento_calendario' inicializado.")

        self.link_adquirente_mantenimiento_tasa_cambio = page.get_by_role("link", name="Mantenimiento Tasa de Cambio")
        self.log.debug(f"Locator 'link_adquirente_mantenimiento_tasa_cambio' inicializado.")

        # Sub-menú Condiciones Comerciales
        self.sub_menu_condiciones_comerciales = page.get_by_role(role="link", name="Condiciones Comerciales",
                                                                 exact=True)
        self.log.debug(f"Locator 'sub_menu_condiciones_comerciales' inicializado.")

        self.link_condiciones_mantenimiento_condiciones_comerciales = page.get_by_role(role="link",
                                                                                       name="Mantenimiento Condiciones Comerciales",
                                                                                       exact=True)
        self.log.debug(f"Locator 'link_condiciones_mantenimiento_condiciones_comerciales' inicializado.")

        self.link_condiciones_mantenimiento_condiciones_promocionales = page.get_by_role(role="link",
                                                                                         name="Mantenimiento Condiciones Comerciales Promocionales", )
        self.log.debug(f"Locator 'link_condiciones_mantenimiento_condiciones_promocionales' inicializado.")

        self.link_condiciones_reporte_condiciones_comerciales = page.get_by_role(role="link",
                                                                                 name="Reporte Condiciones Comerciales")
        self.log.debug(f"Locator 'link_condiciones_reporte_condiciones_comerciales' inicializado.")

        # Enlaces finales de Adquirente
        self.link_adquirente_mantenimiento_grupo_economico = page.get_by_role(role="link",
                                                                              name="Mantenimiento Grupo Económico")
        self.log.debug(f"Locator 'link_adquirente_mantenimiento_grupo_economico' inicializado.")

        self.link_adquirente_mantenimiento_actividad_economica = page.get_by_role(role="link",
                                                                                  name="Mantenimiento Actividad Económica", )
        self.log.debug(f"Locator 'link_adquirente_mantenimiento_actividad_economica' inicializado.")
        self.link_adquirente_mantenimiento_parametros_calculo_mdr = page.get_by_role(role="link",
                                                                                     name="Mantenimiento Parámetros Cálculo MDR")
        self.log.debug(f"Locator 'link_adquirente_mantenimiento_parametros_calculo_mdr' inicializado.")

        self.log.debug(f"Estructura Adquirente (ABCUC) mapeada. {len(self.__dict__)} enlaces detectados.")
        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def _obtener_pasos_para_adquirente(self):
        self.log.debug("Encadenando: Abrir Configuración > Adquirente.")
        return [
            self._obtener_paso_abrir_menu_configuracion(),
            lambda: self.hover(self.sub_menu_adquirente, desc="Sub-menú Adquirente"),
        ]

    def _obtener_pasos_para_terminales(self):
        self.log.debug("Encadenando: Abrir Configuración > Adquirente > Marcas y Modelos de Terminales.")
        return self._obtener_pasos_para_adquirente() + [
            lambda: self.hover(self.sub_menu_terminales, desc="Sub-menú Terminales"),
        ]

    def _obtener_pasos_para_productos(self):
        self.log.debug("Encadenando: Abrir Configuración > Adquirente > Productos.")
        return self._obtener_pasos_para_adquirente() + [
            lambda: self.hover(self.sub_menu_producto, desc="Sub-menú Producto"),
        ]

    def _obtener_pasos_para_condiciones_comerciales(self):
        self.log.debug("Encadenando: Abrir Configuración > Adquirente > Condiciones Comerciales.")
        return self._obtener_pasos_para_adquirente() + [
            lambda: self.hover(self.sub_menu_condiciones_comerciales, desc="Sub-menú Condiciones Comerciales"),
        ]

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_adquirente_marcas_y_modelos_terminales(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Marcas y Modelos de Terminales'."""
        self.log.info(f"Iniciando navegación a 'Marcas y Modelos de Terminales' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_adquirente() + [
            lambda: self.click(self.link_adquirente_marcas_y_modelos_terminales,
                               desc="Link Marcas y Modelos de Terminales")
        ]
        self.log.info(f"Destino: ABCUC022  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ABCUC022",
            locator_titulo_pagina=self.page.locator("h3").get_by_text("Marcas y modelos de terminales"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Adquirente_Marcas_Modelos_Terminales",
        )

    def navegar_a_terminales_alta_terminal(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta de Terminal'."""
        self.log.info(f"Iniciando navegación a 'Alta de Terminal' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_terminales() + [
            lambda: self.click(self.link_terminales_alta_terminal, desc="Link Alta de Terminal"),
        ]
        self.log.info(f"Destino: ABCUC023  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ABCUC023",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Alta de Terminales"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Terminales_Alta_Terminal",
        )

    def navegar_a_terminales_mantenimiento_terminales(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de Terminales'."""
        self.log.info(f"Iniciando navegación a 'Mantenimiento de Terminales' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_terminales() + [
            lambda: self.click(self.link_terminales_mantenimiento_terminales, desc="Link Mantenimiento de Terminales")
        ]
        self.log.info(f"Destino: ABCUC024  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ABCUC024",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Mantenimiento de Terminales"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Terminales_Mantenimiento_Terminales",
        )

    def navegar_a_terminales_alta_masiva_terminales(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta Masiva de Terminales'."""
        self.log.info(f"Iniciando navegación a 'Alta Masiva de Terminales' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_terminales() + [
            lambda: self.click(self.link_terminales_alta_masiva_terminales, desc="Link Alta Masiva de Terminales"),
        ]
        self.log.info(f"Destino: ABCUC039  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ABCUC039",
            locator_titulo_pagina=self.page.locator("h3").get_by_text("Alta Masiva de Terminales"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Terminales_Alta_Masiva_Terminales",
        )

    def navegar_a_terminales_consulta_stock_terminales(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Consulta Stock de Terminales'."""
        self.log.info(f"Iniciando navegación a 'Consulta Stock de Terminales' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_terminales() + [
            lambda: self.click(self.link_terminales_consulta_stock_terminales,
                               desc="Link Consulta Stock de Terminales"),
        ]
        self.log.info(f"Destino: Check-Terminal-Stock  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="Check-Terminal-Stock",
            locator_titulo_pagina=self.page.locator("h3").get_by_text("Consulta Stock de Terminales"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Terminales_Consulta_Stock_Terminales",
        )

    def navegar_a_productos_alta_producto(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Alta de Producto'."""
        self.log.info(f"Iniciando navegación a 'Alta de Producto' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_productos() + [
            lambda: self.click(self.link_producto_alta_producto, desc="Link Alta de Producto"),
        ]
        self.log.info(f"Destino: ABCUC025_AddProduct  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ABCUC025_AddProduct",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Consulta de Producto"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Productos_Alta_Producto",
        )

    def navegar_a_productos_mantenimiento_producto(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de Producto'."""
        self.log.info(f"Iniciando navegación a 'Mantenimiento de Producto' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_productos() + [
            lambda: self.click(self.link_producto_mantenimiento_producto, desc="Link Mantenimiento de Producto"),
        ]
        self.log.info(
            f"Destino: ABCUC025_ModifyProduct  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ABCUC025_ModifyProduct",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Consulta de Producto"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Productos_Mantenimiento_Producto",
        )

    def navegar_a_adquirente_mantenimiento_calendario(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de Calendario Adquirente'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento de Calendario Adquirente' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_adquirente() + [
            lambda: self.click(self.link_adquirente_mantenimiento_calendario,
                               desc="Link Mantenimiento de Calendario Adquirente"),
        ]
        self.log.info(f"Destino: ABCUC015  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ABCUC015",
            locator_titulo_pagina=self.page.locator("h3").get_by_text("Mantenimiento de Calendario"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Adquirente_Mantenimiento_Calendario",
        )

    def navegar_a_adquirente_mantenimiento_tasa_cambio(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento Tasa de Cambio'."""
        self.log.info(f"Iniciando navegación a 'Mantenimiento Tasa de Cambio' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_adquirente() + [
            lambda: self.click(self.link_adquirente_mantenimiento_tasa_cambio,
                               desc="Link Mantenimiento Tasa de Cambio"),
        ]
        self.log.info(f"Destino: ABCUC016  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ABCUC016",
            locator_titulo_pagina=self.page.locator("span").get_by_text("Mantenimiento Tasa de Cambio"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Adquirente_Mantenimiento_Tasa_Cambio",
        )

    def navegar_a_condiciones_mantenimiento_condiciones_comerciales(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de Condiciones Comerciales'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento de Condiciones Comerciales' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_condiciones_comerciales() + [
            lambda: self.click(self.link_condiciones_mantenimiento_condiciones_comerciales,
                               desc="Link Mantenimiento de Condiciones Comerciales"),
        ]
        self.log.info(f"Destino: AMUC016  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMUC016",
            locator_titulo_pagina=self.page.locator("h3").get_by_text("Lista de Condiciones Comerciales"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Condiciones_Mantenimiento_Condiciones_Comerciales",
        )

    def navegar_a_condiciones_mantenimiento_condiciones_promocionales(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento Condiciones Comerciales Promocionales'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento Condiciones Comerciales Promocionales' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_condiciones_comerciales() + [
            lambda: self.click(self.link_condiciones_mantenimiento_condiciones_promocionales,
                               desc="Link Mantenimiento de Condiciones Promocionales")
        ]
        self.log.info(f"Destino: AMRUC045  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMRUC045",
            locator_titulo_pagina=self.page.locator("h3").get_by_text(text="Condiciones Comerciales Promocionales"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Condiciones_Mantenimiento_Condiciones_Promocionales",
        )

    def navegar_a_condiciones_reporte_condiciones_comerciales(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Reporte Condiciones Comerciales'."""
        self.log.info(f"Iniciando navegación a 'Reporte Condiciones Comerciales' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_condiciones_comerciales() + [
            lambda: self.click(self.link_condiciones_reporte_condiciones_comerciales,
                               desc="Link Reporte de Condiciones Comerciales"),
        ]
        self.log.info(f"Destino: AMRUC047  Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="AMRUC047",
            locator_titulo_pagina=self.page.locator("h3").get_by_text(text="Reporte Condiciones Comerciales"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Condiciones_Reporte_Condiciones_Comerciales"
        )

    def navegar_a_adquirente_mantenimiento_grupo_economico(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento Grupo Económico'."""
        self.log.info(f"Iniciando navegación a 'Mantenimiento Grupo Económico' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_adquirente() + [
            lambda: self.click(self.link_adquirente_mantenimiento_grupo_economico,
                               desc="Link Mantenimiento de Grupo Económico"),
        ]
        self.log.info(f"Destino: ABCUC046 Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ABCUC046",
            locator_titulo_pagina=self.page.locator("h3").get_by_text(text="Mantenimiento Grupo Económico"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Adquirente_Mantenimiento_Grupo_Economico"
        )

    def navegar_a_adquirente_mantenimiento_actividad_economica(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento de Actividad Económica'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento de Actividad Económica' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_adquirente() + [
            lambda: self.click(self.link_adquirente_mantenimiento_actividad_economica,
                               desc="Link Mantenimiento de Actividad Económica"),
        ]
        self.log.info(f"Destino: ABCUC047 Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="ABCUC047",
            locator_titulo_pagina=self.page.locator("h3").get_by_text(text="Mantenimiento de Actividad Económica"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Adquirente_Mantenimiento_Actividad_Economica"
        )

    def navegar_a_adquirente_mantenimiento_parametros_calculo_mdr(self, nombre_caso_prueba: str) -> str:
        """Navega a la página 'Mantenimiento Parámetros Cálculo MDR'."""
        self.log.info(
            f"Iniciando navegación a 'Mantenimiento Parámetros Cálculo MDR' para el caso: '{nombre_caso_prueba}'.")
        pasos = self._obtener_pasos_para_adquirente() + [
            lambda: self.click(self.link_adquirente_mantenimiento_parametros_calculo_mdr,
                               desc="Link Mantenimiento de Parámetros Cálculo MDR"),
        ]
        self.log.info(f"Destino: mdr-brand-parameters Ejecutando secuencia de navegación para '{nombre_caso_prueba}'")
        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="mdr-brand-parameters",
            locator_titulo_pagina=self.page.locator("h3").get_by_text(text="Mantenimiento Parámetros Cálculo MDR"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Adquirente_Mantenimiento_Parametros_Calculo_MDR"
        )
