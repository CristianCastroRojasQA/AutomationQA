from playwright.sync_api import Page

from pages.configuracion.adquirente.base_catalogo_page import BaseCatalogoPage


class MarcasPage(BaseCatalogoPage):
    """
    Page Object para la sección de 'Marcas' (Pantalla ABCUC022).
    Hereda toda la funcionalidad del catálogo base.
    """

    # ------------------------------------------------------------------
    # Constantes específicas de Marcas
    # ------------------------------------------------------------------
    SECTION_TITLE = "Marcas"
    INPUT_MAX_LENGTH = "60"

    WARNING_DUPLICADO_TEXT = "Existe una marca con ese nombre"
    ERROR_ELIMINAR_RELACION_TEXT = (
        "No es posible eliminar la Marca, la misma está relacionada a un Modelo de Terminal"
    )

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------
    def __init__(self, page: Page):
        super().__init__(page, logger_name="MarcasPage")
        self.log.debug(
            f"Cargando configuración específica para Marcas (ABCUC022). "
            f"MaxLen: {self.INPUT_MAX_LENGTH}"
        )
        self.log.info(
            "Contexto de 'Marcas' establecido. "
            "Selectores vinculados a la sección ABCUC022."
        )
