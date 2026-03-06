# pages/menu/menu_configuracion_page.py
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.screenshots import capturar_evidencia


class MenuConfiguracionPage(BasePage):
    """
    Page Object para la rama de 'Configuración'.
    Mapeado exactamente según el orden y texto del código fuente.
    """

    def __init__(self, page: Page):
        super().__init__(page, logger_name="MenuConfiguracion")

        # ======================================================================
        # NIVEL 1: RAÍZ
        # ======================================================================
        self.menu_configuracion = page.locator("#CONFIGURATION_KEY")  # Configuración

        # ======================================================================
        # NIVEL 2: ADQUIRENTE (Sub-dropdown)
        # ======================================================================
        self.sub_adquirente = page.locator("#ACQUIRER_CONFIGURATION_KEY")  # Adquirente

        # NIVEL 3 Y 4: DENTRO DE ADQUIRENTE
        # ----------------------------------------------------------------------
        self.link_marcas_y_modelos = page.locator(
            "#ANG_SC_ABCUC022_TTradeAndModel"
        )  # Marcas y Modelos de Terminales

        # Sub-menú Terminales
        self.sub_terminales = page.locator("#TERMINAL_MENU_KEY")  # Terminales
        self.link_alta_terminal = page.locator(
            "#ABCUC023_SaveTerminal"
        )  # Alta de Terminal
        self.link_mantenimiento_terminales = page.locator(
            "#ABCUC024_UpdateTerminalSearch"
        )  # Mantenimiento de Terminales
        self.link_alta_masiva_terminales = page.locator(
            "#ANG_SC_ABCUC039"
        )  # Alta Masiva de Terminales
        self.link_consulta_stock_terminales = page.locator(
            "#ANG_SC_Check-Terminal-Stock"
        )  # Consulta Stock de Terminales

        # Sub-menú Producto
        self.sub_producto = page.locator("#PRODUCT_KEY")  # Producto
        self.link_alta_producto = page.locator(
            "#ABCUC025_AddProduct"
        )  # Alta de Producto
        self.link_mantenimiento_producto = page.locator(
            "#ABCUC025_ModifyProduct"
        )  # Mantenimiento de Producto

        # Enlaces directos en Adquirente
        self.link_mantenimiento_calendario = page.locator(
            "#ANG_SC_ABCUC015_AcqCal_Search"
        )  # Mantenimiento Calendario Adquirente
        self.link_mantenimiento_tasa_cambio = page.locator(
            "#ABCUC016_ExchangeRate"
        )  # Mantenimiento Tasa de Cambio

        # Sub-menú Condiciones Comerciales
        self.sub_condiciones_comerciales = page.locator(
            "#SETTLEMENT_MODEL_KEY"
        )  # Condiciones Comerciales
        self.link_mantenimiento_condiciones = page.locator(
            "#ANG_SC_AMUC016"
        )  # Mantenimiento Condiciones Comerciales
        self.link_mantenimiento_condiciones_promo = page.locator(
            "#ANG_SC_AMRUC045"
        )  # Mantenimiento Condiciones Comerciales Promocionales
        self.link_reporte_condiciones = page.locator(
            "#ANG_SC_AMRUC047"
        )  # Reporte Condiciones Comerciales

        # Enlaces finales de Adquirente
        self.link_mantenimiento_grupo_economico = page.locator(
            "#ANG_SC_ABCUC046"
        )  # Mantenimiento Grupo Económico
        self.link_mantenimiento_actividad_economica = page.locator(
            "#ANG_SC_ABCUC047"
        )  # Mantenimiento Actividad Económica
        self.link_mantenimiento_rango_bines = page.locator(
            "#ANG_SC_BinesRangeMaintenance"
        )  # Mantenimiento Rango de Bines
        self.link_mantenimiento_parametros_mdr = page.locator(
            "#ANG_SC_mdr-brand-parameters"
        )  # Mantenimiento Parámetros Cálculo MDR

        # ======================================================================
        # NIVEL 2: GESTIÓN DE LISTAS DE AUTORIZACIÓN (Sub-dropdown)
        # ======================================================================
        self.sub_gestion_listas = page.locator(
            "#AUTHORIZATION_RULE_LIST_KEY"
        )  # Gestión de Listas de Autorización

        # NIVEL 3: DENTRO DE GESTIÓN DE LISTAS
        self.link_alta_lista_reglas = page.locator(
            "#MIUC001_AddAuthRuleList"
        )  # Alta de lista para reglas de autorización
        self.link_mantenimiento_lista_reglas = page.locator(
            "#MIUC002_UpdateAuthListSearch"
        )  # Mantenimiento de lista para reglas de autorización
        self.link_mantenimiento_valores_lista = page.locator(
            "#MIUC003_UpdtAuthListValSearch"
        )  # Mantenimiento de valores de lista para reglas de autorización
        self.link_eliminar_lista_reglas = page.locator(
            "#MIUC004_DeleteAuthList"
        )  # Eliminar lista para reglas de autorizacion

    """
    Método interno de navegación estándar.
    Centraliza la ejecución de pasos (click/hover), la espera de URL,
    la validación visual de la pantalla y la captura de evidencia,
    para evitar repetir esta lógica en cada método de navegación.
    """

    def _ejecutar_navegacion_estandar(
            self, pasos, url_id, locator_titulo, nombre_caso, etiqueta_foto
    ):
        """Encapsula la lógica repetitiva de navegación y validación."""
        # 1. Ejecuta clics/hovers pasados como lista de lambdas
        for paso in pasos:
            paso()

        # 2. Esperas robustas
        self.page.wait_for_url(f"**/{url_id}*", timeout=15000)
        self.page.wait_for_load_state("networkidle")

        # 3. Validación visual y foto
        locator_titulo.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(500)  # Evita capturas en medio de animaciones

        capturar_evidencia(self.page, nombre_caso, f"Pantalla_{etiqueta_foto}")

        self.log.info(f"Navegación exitosa a {url_id}")
        return self.page.url

    """
    Método interno que define los pasos comunes para navegar
    hasta la sección Adquirente desde el menú Configuración.
    Se usa como prefijo reutilizable en varias navegaciones.
    """

    def _pasos_adquirente(self):
        return [
            lambda: self.click(self.menu_configuracion, desc="Menú Configuración"),
            lambda: self.hover(self.sub_adquirente, desc="Sub-menú Adquirente"),
        ]

    """
    Método interno que define los pasos comunes para navegar
    hasta la sección Gestión de Listas de Autorizacion desde el menú Configuración.
    Se usa como prefijo reutilizable en varias navegaciones.
    """

    def _pasos_gestion_listas_autorizacion(self):
        return [
            lambda: self.click(self.menu_configuracion, desc="Menú Configuración"),
            lambda: self.hover(self.sub_gestion_listas, desc="Sub-menú Gestión de Listas de Autorizacion"),
        ]

    """
    Método interno que extiende la navegación de Adquirente
    hasta la sub-sección Terminales.
    Reutiliza los pasos de Adquirente y agrega el hover necesario.
    """

    def _pasos_terminales(self):
        return self._pasos_adquirente() + [
            lambda: self.hover(self.sub_terminales, desc="Sub-menú Terminales"),
        ]

    """
       Método interno que extiende la navegación de Adquirente
       hasta la sub-sección Productos.
       Reutiliza los pasos de Adquirente y agrega el hover necesario.
       """

    def _pasos_productos(self):
        return self._pasos_adquirente() + [
            lambda: self.hover(self.sub_producto, desc="Sub-menú Productos"),
        ]

    """
       Método interno que extiende la navegación de Adquirente
       hasta la sub-sección Productos.
       Reutiliza los pasos de Adquirente y agrega el hover necesario.
       """

    def _pasos_condiciones_comerciales(self):
        return self._pasos_adquirente() + [
            lambda: self.hover(self.sub_condiciones_comerciales, desc="Sub-menú Condiciones Comerciales"),
        ]

    # ----------------------------------------------------------------------
    # Métodos de navegación Configuración Adquirente siguiendo el flujo visual
    # ----------------------------------------------------------------------

    def marca_modelos_terminales(self, nombre_caso: str):
        # Solo agregamos el clic final al prefijo de Adquirente
        pasos = self._pasos_adquirente() + [
            lambda: self.click(self.link_marcas_y_modelos, desc="Link Marcas y Modelos de Terminales")
        ]

        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="ABCUC022",
            locator_titulo=self.page.get_by_role("heading", name="Marcas y modelos de terminales"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Marcas_Modelos"
        )

    def terminales_alta_terminal(self, nombre_caso: str):
        pasos = self._pasos_terminales() + [
            lambda: self.click(self.link_alta_terminal, desc="Link Alta de Terminales"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="ABCUC023",
            locator_titulo=self.page.locator("span[id$='titlePageLabel']"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Alta_Terminal",
        )

    def terminales_mantenimiento_terminales(self, nombre_caso: str):
        pasos = self._pasos_terminales() + [
            lambda: self.click(self.link_mantenimiento_terminales, desc="Link Mantenimiento Terminales")
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="ABCUC024",
            locator_titulo=self.page.locator("span[id$='titlePageLabel2']"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Mantenimiento_Terminales",
        )

    def terminales_alta_masiva_terminales(self, nombre_caso: str):
        pasos = self._pasos_terminales() + [
            lambda: self.click(self.link_alta_masiva_terminales, desc="Link Alta Masiva de Terminales"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="ABCUC039",
            locator_titulo=self.page.get_by_role("heading", name="Alta Masiva de Terminales"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Alta_Masiva_Terminales",
        )

    def terminales_consulta_stock_terminales(self, nombre_caso: str):
        pasos = self._pasos_terminales() + [
            lambda: self.click(self.link_consulta_stock_terminales, desc="Link Consulta Stock de Terminales"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="Check-Terminal-Stock",
            locator_titulo=self.page.get_by_role("heading", name="Consulta Stock de Terminales"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Consulta_Stock_Terminales",
        )

    def productos_alta_productos(self, nombre_caso: str):
        pasos = self._pasos_productos() + [
            lambda: self.click(self.link_alta_producto, desc="Link Alta Productos"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="ABCUC025_AddProduct",
            locator_titulo=self.page.locator("span[id$='lblTitleStep1']"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Alta de Productos",
        )

    def productos_mantenimiento_productos(self, nombre_caso: str):
        pasos = self._pasos_productos() + [
            lambda: self.click(self.link_mantenimiento_producto, desc="Link Mantenimiento de Productos"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="ABCUC025_ModifyProduct",
            locator_titulo=self.page.locator("span[id$='lblProductSelecionTitle']"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Matenimiento de Productos",
        )

    def mantenimiento_calendario_adquirente(self, nombre_caso: str):
        pasos = self._pasos_adquirente() + [
            lambda: self.click(self.link_mantenimiento_calendario, desc="Link Mantenimiento de Calendario Adquirente"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="ABCUC015",
            locator_titulo=self.page.get_by_role("heading", name="Mantenimiento de Calendario"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Matenimiento de Calendario Adquirente",
        )

    def mantenimiento_tasa_cambio(self, nombre_caso: str):
        pasos = self._pasos_adquirente() + [
            lambda: self.click(self.link_mantenimiento_tasa_cambio, desc="Link Mantenimiento Tasa de Cambio"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="ABCUC016",
            locator_titulo=self.page.locator("span[id$='lbl_title']"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Matenimiento de Tasa de Cambio",
        )

    def mantenimiento_condiciones_comerciales(self, nombre_caso: str):
        pasos = self._pasos_condiciones_comerciales() + [
            lambda: self.click(self.link_mantenimiento_condiciones,
                               desc="Link Mantenimiento de Condiciones Comerciales"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="AMUC016",
            locator_titulo=self.page.get_by_role("heading", name="Lista de Condiciones Comerciales"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Matenimiento de Condiciones Comerciales",
        )

    def mantenimiento_condiciones_comerciales_promocionales(self, nombre_caso: str):
        pasos = self._pasos_condiciones_comerciales() + [
            lambda: self.click(self.link_mantenimiento_condiciones_promo,
                               desc="Link Mantenimiento de Condiciones Promociales")
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="AMRUC045",
            locator_titulo=self.page.get_by_role("heading", name="Condiciones Comerciales Promocionales"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Mantenimiento de Condiciones Promociales",
        )

    def reporte_condiciones_comerciales(self, nombre_caso: str):
        pasos = self._pasos_condiciones_comerciales() + [
            lambda: self.click(self.link_reporte_condiciones, desc="Link Reporte de Condiciones Comerciales"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="AMRUC047",
            locator_titulo=self.page.get_by_role("heading", name="Reporte Condiciones Comerciales"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Reporte Condiciones Comerciales"
        )

    def mantenimiento_grupo_economico(self, nombre_caso: str):
        pasos = self._pasos_adquirente() + [
            lambda: self.click(self.link_mantenimiento_grupo_economico, desc="Link Mantenimiento de Grupo EConomico"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="ABCUC046",
            locator_titulo=self.page.get_by_role("heading", name="Mantenimiento Grupo Económico"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Mantenimiento de Grupo Economico"
        )

    def mantenimiento_actividad_economica(self, nombre_caso: str):
        pasos = self._pasos_adquirente() + [
            lambda: self.click(self.link_mantenimiento_actividad_economica,
                               desc="Link Mantenimiento de Actividad Economico"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="ABCUC047",
            locator_titulo=self.page.get_by_role("heading", name="Mantenimiento de Actividad Económica"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Mantenimiento de Actividad Económica"
        )

    # Pendiente Creación de la funcion
    # def mantenimiento_rango_bines(self, nombre_caso: str):
    #     pasos = self._pasos_adquirente() + [
    #         lambda:self.click(self.link_mantenimiento_rango_bines, desc="Link Mantenimiento de Rango Bines"),
    #     ]
    #     return self._ejecutar_navegacion_estandar(
    #         pasos=pasos,
    #         url_id="BinesRangeMaintenance",
    #         locator_titulo=se
    #     )

    def mantenimiento_parametros_calculo_mdr(self, nombre_caso: str):
        pasos = self._pasos_adquirente() + [
            lambda: self.click(self.link_mantenimiento_parametros_mdr,
                               desc="Link Mantenimiento de Parametros Calculos MDR"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="mdr-brand-parameters",
            locator_titulo=self.page.get_by_role("heading", name="Mantenimiento Parámetros Cálculo MDR"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Mantenimiento Parámetros Cálculo MDR"
        )

    # ----------------------------------------------------------------------
    # Métodos de navegación Configuración Gestión de Listas de Autorización siguiendo el flujo visual
    # ----------------------------------------------------------------------

    def gestion_alta_lista_reglas_autorizacion(self, nombre_caso: str):
        pasos = self._pasos_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_alta_lista_reglas, desc="Link Alta Lista para Reglas de Autorizacion"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="AddAuthorizationRuleList",
            locator_titulo=self.page.get_by_text("Añadir Lista de Reglas de Autorización", exact=True),
            nombre_caso=nombre_caso,
            etiqueta_foto="Alta Lista para Reglas de Autorizacion"
        )

    def gestion_mantenimiento_lista_reglas_autorizacion(self, nombre_caso: str):
        pasos = self._pasos_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_mantenimiento_lista_reglas,
                               desc="Link Mantenimiento de Lista para Reglas de Autorizacion"),
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="UpdateAuthorizationRuleListSearch",
            locator_titulo=self.page.locator("span[id$='titlePageLabel2']"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Mantenimiento de Lista de Reglas de Autorización"
        )

    def gestion_mantenimiento_valores_lista_reglas_autorizacion(self, nombre_caso: str):
        pasos = self._pasos_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_mantenimiento_valores_lista,
                               desc="Link Mantenimiento de Valores de Lista para Reglas de Autorización")
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="UpdateAuthorizationRuleListValuesSearch",
            locator_titulo=self.page.locator("span[id$='titlePageLabel2']"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Mantenimiento de Valores de Lista de Reglas de Autorización"
        )

    def gestion_eliminar_listas_reglas_autorizacion(self, nombre_caso: str):
        pasos = self._pasos_gestion_listas_autorizacion() + [
            lambda: self.click(self.link_eliminar_lista_reglas, desc="link Eliminar Lista para Reglas de autorización")
        ]
        return self._ejecutar_navegacion_estandar(
            pasos=pasos,
            url_id="DeleteAuthorizationRuleList",
            locator_titulo=self.page.locator("span[id$='titlePageLabel2']"),
            nombre_caso=nombre_caso,
            etiqueta_foto="Eliminar Lista para Reglas de autorización"
        )
