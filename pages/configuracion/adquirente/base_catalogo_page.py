from abc import ABC
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class BaseCatalogoPage(BasePage, ABC):
    """
    Page Object abstracto para catálogos genéricos.
    Proporciona la estructura base para pantallas con secciones de gestión,
    grids de datos y formularios de entrada.
    """

    # ------------------------------------------------------------------
    # Propiedades Abstractas (Deberán definirse en la clase hija)
    # ------------------------------------------------------------------
    SECTION_TITLE: str  # Título de la sección (ej: "Marcas")
    INPUT_MAX_LENGTH: str  # Longitud máxima permitida en el input
    WARNING_DUPLICADO_TEXT: str  # Texto de alerta para registros duplicados
    ERROR_ELIMINAR_RELACION_TEXT: str  # Texto de error por integridad referencial

    # ------------------------------------------------------------------
    # Constantes de Aplicación
    # ------------------------------------------------------------------
    SUCCESS_TEXT = "Marcas y Modelos actualizados correctamente"

    # ------------------------------------------------------------------
    # Constructor e Inicialización
    # ------------------------------------------------------------------
    def __init__(self, page: Page, logger_name: str):
        super().__init__(page, logger_name=logger_name)
        self.page = page

        # Contenedor principal delimitado por el título de sección
        self.seccion_contenedor = self.page.locator(
            "div.custom-titles-width",
            has=self.page.locator("h5", has_text=self.SECTION_TITLE)
        )

        # Botones de Acción Global (Pantalla completa)
        self.btn_guardar = self.page.locator(
            "app-button .btn.btn-info",
            has_text="Guardar"
        )
        self.btn_cancelar = self.page.locator(
            "app-button .btn",
            has_text="Cancelar"
        )

        # Controles de Paginación (Internos a la sección)
        self.btn_siguiente = self.seccion_contenedor.locator("button .icon-step-forward")
        self.btn_ultima_pag = self.seccion_contenedor.locator("button .icon-fast-forward")
        self.paginador_info = self.seccion_contenedor.locator(".cart-datagrid-pager-text")

        # Alertas y Feedback del Sistema
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
    # Locators Dinámicos
    # ------------------------------------------------------------------
    def input_principal(self) -> Locator:
        """Input de texto principal del formulario."""
        return self.seccion_contenedor.locator(
            f'input[type="text"][maxlength="{self.INPUT_MAX_LENGTH}"]'
        )

    def btn_incluir(self) -> Locator:
        """Botón para agregar un nuevo registro a la tabla."""
        return self.seccion_contenedor.locator("div.btn.btn-small", has_text="Incluir")

    def btn_eliminar(self) -> Locator:
        """Botón para quitar el registro seleccionado."""
        return self.seccion_contenedor.locator("div.btn.btn-small", has_text="Eliminar")

    def msg_error_campo(self) -> Locator:
        """Mensaje de error asociado a la validación del input."""
        return self.seccion_contenedor.locator("app-control-error-message")

    def grid_cells(self) -> Locator:
        """Celdas de datos dentro del grid (Wijmo)."""
        return self.seccion_contenedor.locator('wj-flex-grid [role="gridcell"]')

    # ------------------------------------------------------------------
    # Acciones (Verbos)
    # ------------------------------------------------------------------
    def escribir_valor(self, texto: str):
        """Escribe el texto proporcionado en el input principal."""
        self.log.info(f"[FILL] Valor = '{texto}'")
        expect(self.seccion_contenedor).to_be_visible()
        self.input_principal().fill(texto)

    def click_incluir(self):
        """Ejecuta el click en el botón de inclusión de la sección."""
        self.log.info("[CLICK] Incluir")
        self.btn_incluir().click()

    def seleccionar_registro_en_grid(self, texto: str):
        """Busca y selecciona una fila en el grid basándose en el texto."""
        self.log.info(f"[GRID] Seleccionar fila con texto: '{texto}'")
        self.grid_cells().filter(has_text=texto).first.click()

    def click_eliminar(self):
        """Ejecuta el click en el botón de eliminación de la sección."""
        self.log.info("[CLICK] Eliminar")
        self.btn_eliminar().click()

    def click_guardar(self):
        """Click en el botón Guardar general de la pantalla."""
        self.log.info("[CLICK] Guardar global")
        self.btn_guardar.click()

    def click_cancelar(self):
        """Click en el botón Cancelar general de la pantalla."""
        self.log.info("[CLICK] Cancelar global")
        self.btn_cancelar.click()

    def recargar_pagina(self):
        """Refresca el sitio para verificar persistencia de datos."""
        self.log.info("[ACTION] Recargar página")
        self.page.reload()
        self.page.wait_for_load_state("domcontentloaded")

    # ------------------------------------------------------------------
    # Consultas de Estado (Queries)
    # ------------------------------------------------------------------
    def obtener_conteo_grid(self) -> int:
        """Retorna la cantidad de celdas/registros visibles en el grid."""
        return self.grid_cells().count()

    def esta_registro_visible(self, texto: str) -> bool:
        """Verifica si un registro específico existe en la vista actual del grid."""
        return self.grid_cells().filter(has_text=texto).count() > 0

    def obtener_valor_input(self) -> str:
        """Captura el texto actual del campo de entrada."""
        return self.input_principal().input_value()

    def es_boton_eliminar_deshabilitado(self) -> bool:
        """Evalúa si el botón eliminar tiene estado deshabilitado por CSS."""
        cls = self.btn_eliminar().get_attribute("class") or ""
        return "disabled" in cls

    def es_input_invalido(self) -> bool:
        """Verifica si el input tiene la clase de error de Angular (ng-invalid)."""
        cls = self.input_principal().get_attribute("class") or ""
        return "ng-invalid" in cls

    # ------------------------------------------------------------------
    # Sincronización y Esperas de UI
    # ------------------------------------------------------------------
    def esperar_alerta_exito(self, timeout_ms: int = 15000):
        """Espera el mensaje de éxito y realiza scroll al inicio."""
        self.log.info("[WAIT] Alert Success")
        expect(self.alert_success).to_be_visible(timeout=timeout_ms)
        self.page.evaluate("window.scrollTo(0, 0)")

    def es_alerta_exito_visible(self) -> bool:
        """Comprobación inmediata de visibilidad del mensaje de éxito."""
        return self.alert_success.count() > 0 and self.alert_success.first.is_visible()

    def esperar_alerta_duplicado(self, timeout_ms: int = 15000):
        """Espera el mensaje de advertencia por duplicidad."""
        self.log.info("[WAIT] Alert Warning Duplicado")
        expect(self.alert_warning_duplicado).to_be_visible(timeout=timeout_ms)
        self.page.evaluate("window.scrollTo(0, 0)")

    # ------------------------------------------------------------------
    # Navegación y Búsqueda Avanzada
    # ------------------------------------------------------------------
    def buscar_en_paginacion(self, texto: str) -> bool:
        """
        Navega por las páginas del grid buscando un registro específico.
        Retorna True si lo encuentra, False si llega al final sin éxito.
        """
        self.log.info(f"[SEARCH] Iniciando búsqueda de '{texto}' en el paginado...")

        while True:
            if self.grid_cells().filter(has_text=texto).count() > 0:
                self.log.info(f"[SEARCH] Registro '{texto}' encontrado.")
                return True

            if self.btn_siguiente.is_disabled():
                self.log.warning(f"[SEARCH] Fin de tabla. No se encontró: '{texto}'")
                return False

            self.log.info("[SEARCH] No presente en esta página. Avanzando...")
            self.btn_siguiente.click()
            self.page.wait_for_timeout(500)  # Pausa para refresco de DOM en Wijmo
