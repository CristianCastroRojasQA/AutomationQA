from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class MarcasPage(BasePage):
    """
    Page Object para la sección de 'Marcas' (Pantalla ABCUC022).
    Se enfoca en localizar elementos y realizar acciones básicas (escribir, click).
    """

    # ------------------------------------------------------------------
    # Constantes / Textos esperados (para validaciones rápidas)
    # ------------------------------------------------------------------
    SUCCESS_TEXT = "Marcas y Modelos actualizados correctamente"
    WARNING_DUPLICADO_TEXT = "Existe una marca con ese nombre"
    ERROR_ELIMINAR_RELACION_TEXT = (
        "No es posible eliminar la Marca, la misma está relacionada a un Modelo de Terminal"
    )

    # ------------------------------------------------------------------
    # Constructor / Inicialización de Locators base
    # ------------------------------------------------------------------
    def __init__(self, page: Page):
        super().__init__(page, logger_name="MarcasPage")
        self.page = page

        # SCOPE: Limitamos la búsqueda al div que contiene el título "Marcas"
        self.seccion_marcas = self.page.locator(
            "div.custom-titles-width",
            has=self.page.locator("h5", has_text="Marcas")
        )

        # -----------------------------
        # Botones globales (pantalla)
        # -----------------------------
        self.btn_guardar = self.page.locator(
            "app-button .btn.btn-info",
            has_text="Guardar"
        )

        self.btn_cancelar = self.page.locator(
            "app-button .btn",
            has_text="Cancelar"
        )

        # -----------------------------
        # Paginación (dentro de Marcas)
        # -----------------------------
        self.btn_siguiente = self.seccion_marcas.locator("button .icon-step-forward")
        self.btn_ultima_pag = self.seccion_marcas.locator("button .icon-fast-forward")
        self.paginador_info = self.seccion_marcas.locator(".cart-datagrid-pager-text")

        # -----------------------------
        # Alertas / feedback sistema
        # -----------------------------
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

    # ------------------------------------------------------------------
    # Locators dinámicos (se evalúan al momento de uso)
    # ------------------------------------------------------------------
    def input_marca(self) -> Locator:
        """Input de marca dentro del contenedor Marcas."""
        return self.seccion_marcas.locator('input[type="text"][maxlength="60"]')

    def btn_incluir(self) -> Locator:
        """Botón Incluir del bloque Marcas."""
        return self.seccion_marcas.locator("div.btn.btn-small", has_text="Incluir")

    def btn_eliminar(self) -> Locator:
        """Botón Eliminar del bloque Marcas."""
        return self.seccion_marcas.locator("div.btn.btn-small", has_text="Eliminar")

    def msg_error_campo(self) -> Locator:
        """Mensaje de validación de campo (ej: 'Campo requerido')."""
        return self.seccion_marcas.locator("app-control-error-message")

    def grid_cells(self) -> Locator:
        """Celdas del grid de Marcas."""
        return self.seccion_marcas.locator('wj-flex-grid [role="gridcell"]')

    # ------------------------------------------------------------------
    # Acciones (verbos)
    # ------------------------------------------------------------------
    def escribir_marca(self, nombre: str):
        self.log.info(f"[FILL] Marca = '{nombre}'")
        expect(self.seccion_marcas).to_be_visible()  # Verifica que la sección cargó
        self.input_marca().fill(nombre)

    def click_incluir(self):
        self.log.info("[CLICK] Incluir (bloque Marcas)")
        self.btn_incluir().click()

    def seleccionar_marca_en_grid(self, nombre: str):
        self.log.info(f"[CLICK] Seleccionar marca en grid = '{nombre}'")
        # Filtra la tabla por el texto y hace click en la primera coincidencia
        celda = self.grid_cells().filter(has_text=nombre).first
        celda.click()

    def click_eliminar(self):
        self.log.info("[CLICK] Eliminar (bloque Marcas)")
        self.btn_eliminar().click()

    def click_guardar(self):
        self.log.info("[CLICK] Guardar (global)")
        self.btn_guardar.click()

    def click_cancelar(self):
        self.log.info("[CLICK]  Cancelar (global)")
        self.btn_cancelar.click()

    def recargar(self):
        """Fuerza una recarga del navegador para validar persistencia."""
        self.log.info("[ACTION] Reload página")
        self.page.reload()
        self.page.wait_for_load_state("domcontentloaded")

    # ------------------------------------------------------------------
    # Lecturas / Estado (queries)
    # ------------------------------------------------------------------
    def cantidad_marcas(self) -> int:
        return self.grid_cells().count()

    def marca_visible(self, nombre: str) -> bool:
        """Retorna True si el nombre existe en la tabla."""
        return self.grid_cells().filter(has_text=nombre).count() > 0

    def valor_input(self) -> str:
        """Retorna el texto actual dentro del campo de entrada."""
        return self.input_marca().input_value()

    def eliminar_deshabilitado(self) -> bool:
        """Verifica si el botón eliminar tiene la clase 'disabled'."""
        cls = self.btn_eliminar().get_attribute("class") or ""
        return "disabled" in cls

    def input_es_invalido(self) -> bool:
        """Detecta si Angular marcó el campo como inválido (ng-invalid)."""
        cls = self.input_marca().get_attribute("class") or ""
        return "ng-invalid" in cls

    # ------------------------------------------------------------------
    # Esperas activas (esperas robustas de UI)
    # ------------------------------------------------------------------
    def esperar_success(self, timeout_ms: int = 15000):
        self.log.info("[WAIT] Alert success")
        expect(self.alert_success).to_be_visible(timeout=timeout_ms)
        # Hacer scroll al inicio (0,0) de la página inmediatamente
        self.log.info("[ACTION] Scroll al inicio de la página")
        self.page.evaluate("window.scrollTo(0, 0)")

    def success_visible(self) -> bool:
        """Verificación rápida sin esperar timeout largo."""
        return self.alert_success.count() > 0 and self.alert_success.first.is_visible()

    def esperar_warning_duplicado(self, timeout_ms: int = 15000):
        self.log.info("[WAIT] Alert warning duplicado")
        expect(self.alert_warning_duplicado).to_be_visible(timeout=timeout_ms)
        self.log.info("[ACTION] Scroll al inicio de la página")
        self.page.evaluate("window.scrollTo(0, 0)")

    # ------------------------------------------------------------------
    # Utilidades: Búsqueda en paginación
    # ------------------------------------------------------------------
    def buscar_marca_en_paginacion(self, nombre: str) -> bool:
        """
        Recorre las páginas del grid buscando el texto hasta encontrarlo o agotar páginas.
        """
        self.log.info(f"[SEARCH] Buscando '{nombre}' en el grid...")

        while True:
            # Check en la página actual
            if self.grid_cells().filter(has_text=nombre).count() > 0:
                self.log.info("[SEARCH] Encontrado en página actual.")
                return True

            # Si no está y el botón siguiente está deshabilitado, no existe
            if self.btn_siguiente.is_disabled():
                self.log.warning(f"[SEARCH] Fin de paginación. '{nombre}' no encontrado.")
                return False

            # Click en siguiente y pequeña espera para que el DOM refresque
            self.log.info("[SEARCH] No está en esta página. Click en 'Siguiente'...")
            self.btn_siguiente.click()
            self.page.wait_for_timeout(500)  # Tiempo para que Wijmo repinte las celdas
