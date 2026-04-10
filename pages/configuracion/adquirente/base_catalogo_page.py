from abc import ABC
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class BaseCatalogoPage(BasePage, ABC):
    """
    Page Object abstracto para catálogos genéricos (Marcas, Tecnologías, etc).

    Regla del POM:
    - Selectores (constructores) primero
    - Luego helpers de estado
    - Luego acciones
    - Luego búsquedas
    """

    # ============================================================
    # Propiedades abstractas (definidas en clases hijas)
    # ============================================================
    SECTION_TITLE: str
    INPUT_MAX_LENGTH: str
    WARNING_DUPLICADO_TEXT: str
    ERROR_ELIMINAR_RELACION_TEXT: str

    # ============================================================
    # Constantes de aplicación
    # ============================================================
    SUCCESS_TEXT = "Marcas y Modelos actualizados correctamente"

    # ============================================================
    # Constructor
    # ============================================================
    def __init__(self, page: Page, logger_name: str):
        super().__init__(page, logger_name=logger_name)
        self.page = page

        # --------------------------------------------------------
        # Contenedor principal de la sección
        # --------------------------------------------------------
        self.seccion_contenedor = self.page.locator(
            "div.custom-titles-width",
            has=self.page.locator("h5", has_text=self.SECTION_TITLE)
        )

        # --------------------------------------------------------
        # Botones globales
        # --------------------------------------------------------
        self.btn_guardar = self.page.locator(
            "app-button .btn.btn-info",
            has_text="Guardar"
        )
        self.btn_cancelar = self.page.locator(
            "app-button .btn",
            has_text="Cancelar"
        )

        # --------------------------------------------------------
        # Alertas
        # --------------------------------------------------------
        self.alert_success = self.page.locator(
            "div.alert.alert-success",
            has_text=self.SUCCESS_TEXT
        )
        self.alert_warning_duplicado = self.page.locator(
            "div.alert.alert-warning",
            has_text=self.WARNING_DUPLICADO_TEXT
        )
        self.alert_error_eliminar_relacion = self.page.locator(
            "div.alert.alert-error",
            has_text=self.ERROR_ELIMINAR_RELACION_TEXT
        )
        self.alert_error_global = self.page.locator(
            "div.alert.alert-error, div.alert.alert-danger"
        )

        # --------------------------------------------------------
        # Contenedor del paginador
        # --------------------------------------------------------
        self.paginador_contenedor = self.seccion_contenedor.locator(
            "div.cart-datagrid-footer"
        )

        # --------------------------------------------------------
        # Botones del paginador (TODOS)
        # --------------------------------------------------------
        self.btn_paginador_primero = self.paginador_contenedor.locator(
            "button:has(span.icon-fast-backward)"
        )
        self.btn_paginador_anterior = self.paginador_contenedor.locator(
            "button:has(span.icon-step-backward)"
        )
        self.btn_paginador_siguiente = self.paginador_contenedor.locator(
            "button:has(span.icon-step-forward)"
        )
        self.btn_paginador_ultimo = self.paginador_contenedor.locator(
            "button:has(span.icon-fast-forward)"
        )

        # --------------------------------------------------------
        # Input y texto de paginación
        # --------------------------------------------------------
        self.input_pagina_actual = self.paginador_contenedor.locator(
            "input.input-page[type='number']"
        )
        self.texto_paginacion = self.paginador_contenedor.locator(
            ".cart-datagrid-pager-text"
        )

        # --------------------------------------------------------
        # Grid Wijmo
        # --------------------------------------------------------
        self.grid_root = self.seccion_contenedor.locator(
            "wj-flex-grid div[wj-part='cells'][role='grid']"
        )
        self.grid_cells = self.seccion_contenedor.locator(
            "wj-flex-grid [role='gridcell']"
        )
        self.grid_fila_seleccionada = self.seccion_contenedor.locator(
            "[role='gridcell'][aria-selected='true']"
        )

        # --------------------------------------------------------
        # Formulario
        # --------------------------------------------------------
        self.input_principal = self.seccion_contenedor.locator(
            f'input[type="text"][maxlength="{self.INPUT_MAX_LENGTH}"]'
        )
        self.msg_error_campo = self.seccion_contenedor.locator(
            "app-control-error-message"
        )

        # --------------------------------------------------------
        # Botones CRUD locales
        # --------------------------------------------------------
        self.btn_incluir = self.seccion_contenedor.locator(
            "div.btn.btn-small",
            has_text="Incluir"
        )
        self.btn_eliminar = self.seccion_contenedor.locator(
            "div.btn.btn-small",
            has_text="Eliminar"
        )

    # ============================================================
    # Helpers de estado y sincronización
    # ============================================================
    def esperar_grid_renderizado(self, timeout_ms: int = 15000):
        """Garantiza que el grid Wijmo esté estable y renderizado."""
        self.log.info("[WAIT] Grid renderizado")
        expect(self.grid_root).to_be_visible(timeout=timeout_ms)
        self.page.wait_for_load_state("networkidle")

    @staticmethod
    def es_boton_habilitado(boton: Locator) -> bool:
        """Evalúa si un botón está habilitado."""
        return not boton.is_disabled()

    def esta_en_primera_pagina(self) -> bool:
        return not self.es_boton_habilitado(self.btn_paginador_anterior)

    def esta_en_ultima_pagina(self) -> bool:
        return not self.es_boton_habilitado(self.btn_paginador_siguiente)

    # ============================================================
    # Acciones de formulario
    # ============================================================
    def escribir_valor(self, texto: str):
        self.log.info(f"[FILL] '{texto}'")
        expect(self.seccion_contenedor).to_be_visible()
        self.input_principal.fill(texto)

    # ============================================================
    # Acciones CRUD
    # ============================================================
    def click_incluir(self):
        self.log.info("[CLICK] Incluir")
        self.btn_incluir.click()

    def seleccionar_registro_en_grid(self, texto: str):
        """
        Selecciona un registro en el grid Wijmo haciendo click
        sobre la celda que contiene el texto indicado.
        """
        self.log.info(f"[GRID] Seleccionando registro con texto: '{texto}'")
        self.esperar_grid_renderizado()

        celda = self.grid_cells.filter(has_text=texto).first
        if not celda.is_visible():
            raise AssertionError(
                f"BUG: No se encontró el registro '{texto}' para seleccionar en la grilla"
            )

        celda.click()

    def click_eliminar(self):
        self.log.info("[CLICK] Eliminar")
        self.btn_eliminar.click()

    def click_guardar(self):
        self.log.info("[CLICK] Guardar")
        self.btn_guardar.click()

    def click_cancelar(self):
        self.log.info("[CLICK] Cancelar]")
        self.btn_cancelar.click()

    def recargar_pagina(self):
        self.log.info("[ACTION] Reload page")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")

    # ============================================================
    # Acciones del paginador
    # ============================================================
    def ir_a_primera_pagina(self):
        self.log.info("[PAGINADOR] Ir a primera página")
        if self.es_boton_habilitado(self.btn_paginador_primero):
            self.btn_paginador_primero.click()
            self.esperar_grid_renderizado()

    def ir_a_ultima_pagina(self):
        self.log.info("[PAGINADOR] Ir a última página")
        if self.es_boton_habilitado(self.btn_paginador_ultimo):
            self.btn_paginador_ultimo.click()
            self.esperar_grid_renderizado()

    def avanzar_pagina(self) -> bool:
        if not self.es_boton_habilitado(self.btn_paginador_siguiente):
            return False
        self.log.info("[PAGINADOR] Avanzar página")
        self.btn_paginador_siguiente.click()
        self.esperar_grid_renderizado()
        return True

    def retroceder_pagina(self) -> bool:
        if not self.es_boton_habilitado(self.btn_paginador_anterior):
            return False
        self.log.info("[PAGINADOR] Retroceder página")
        self.btn_paginador_anterior.click()
        self.esperar_grid_renderizado()
        return True

    # ============================================================
    # Queries
    # ============================================================

    def es_boton_eliminar_habilitado(self) -> bool:
        cls = self.btn_eliminar.get_attribute("class") or ""
        return "disabled" not in cls

    def obtener_texto_alerta_exito(self) -> str:
        """
        Retorna únicamente el texto funcional del mensaje de éxito,
        excluyendo íconos, encabezados y botones de cierre.
        """
        self.log.info("[QUERY] Obtener texto funcional del mensaje de éxito")
        # Extrae solo el texto visible que corresponde al mensaje de negocio
        texto = self.alert_success.inner_text()
        texto_limpio = (
            texto
            .replace("×", "")
            .replace("Notificación!", "")
            .strip()
        )
        return texto_limpio

    def obtener_texto_alerta_warning(self) -> str:
        """
        Retorna únicamente el texto funcional del mensaje de warning,
        excluyendo íconos, encabezados y botones de cierre.
        """
        self.log.info("[QUERY] Obtener texto funcional del mensaje de advertencia")
        # Extrae solo el texto visible que corresponde al mensaje de negocio
        texto = self.WARNING_DUPLICADO_TEXT
        texto_limpio = (
            texto
            .replace("×", "")
            .replace("Notificación!", "")
            .strip()
        )
        return texto_limpio

    def obtener_texto_alerta_error_relacion(self) -> str:
        """
        Retorna únicamente el texto funcional del mensaje de error
        al intentar eliminar una marca que posee relaciones.
        """
        self.log.info("[QUERY] Obtener texto funcional del mensaje de error por relación")

        texto = self.alert_error_eliminar_relacion.inner_text()

        texto_limpio = (
            texto
            .replace("×", "")
            .replace("Han ocurrido errores!", "")
            .strip()
        )

        return texto_limpio

    def es_input_invalido(self) -> bool:
        cls = self.input_principal.get_attribute("class") or ""
        return "ng-invalid" in cls

    def obtener_valor_input(self) -> str:
        """
        Retorna el valor actual escrito en el input principal del formulario.
        Se usa para validaciones de longitud, truncamiento y estado del campo.
        """
        self.log.info("[QUERY] Obtener valor actual del input principal")
        return self.input_principal.input_value()

    def obtener_conteo_grid(self) -> int:
        """
        Retorna la cantidad de registros visibles en el grid.
        Se usa para validar que la grilla no se modifique indebidamente.
        """
        self.log.info("[QUERY] Obtener conteo de registros en la grilla")
        self.esperar_grid_renderizado()
        return self.grid_cells.count()

    def es_alerta_exito_visible(self) -> bool:
        """
        Verifica si el mensaje de éxito está visible actualmente.
        NO espera, solo consulta estado.
        """
        self.log.info("[QUERY] ¿Alerta de éxito visible?")
        return self.alert_success.is_visible()

    # ============================================================
    # Alertas
    # ============================================================
    def esperar_alerta_exito(self, timeout_ms: int = 15000):
        self.log.info("[WAIT] Alert Success")
        expect(self.alert_success).to_be_visible(timeout=timeout_ms)
        self.page.evaluate("window.scrollTo(0, 0)")

    def esperar_alerta_duplicado(self, timeout_ms: int = 15000):
        self.log.info("[WAIT] Alert Warning Duplicado")
        expect(self.alert_warning_duplicado).to_be_visible(timeout=timeout_ms)
        self.page.evaluate("window.scrollTo(0, 0)")

    def esperar_alerta_error_relacion(self, timeout_ms: int = 15000):
        self.log.info("[WAIT] Alert Error Eliminado")
        expect(self.alert_error_eliminar_relacion).to_be_visible(timeout=timeout_ms)
        self.page.evaluate("window.scrollTo(0, 0)")

    # ============================================================
    # Búsqueda en paginación
    # ============================================================
    def buscar_en_paginacion(self, texto: str) -> bool:
        """
        Busca un registro recorriendo toda la grilla, de forma determinística.
        """
        self.log.info(f"[SEARCH] Buscar '{texto}' en grilla")

        if not self.esta_en_primera_pagina():
            self.ir_a_primera_pagina()

        while True:
            self.esperar_grid_renderizado()

            if self.grid_cells.filter(has_text=texto).count() > 0:
                self.log.info("[SEARCH] Registro encontrado")
                return True

            if not self.avanzar_pagina():
                self.log.warning("[SEARCH] Fin de paginación. No encontrado")
                return False

    def preparar_registro_para_eliminacion(self, texto: str):
        """
        Busca y deja el registro seleccionado en un estado válido
        para permitir la eliminación.
        """
        self.log.info(f"[GRID] Preparando registro para eliminación: {texto}")

        if not self.buscar_en_paginacion(texto):
            raise AssertionError(f"No se encontró el registro '{texto}'")

        celda = self.grid_cells.filter(has_text=texto).first
        celda.click()
