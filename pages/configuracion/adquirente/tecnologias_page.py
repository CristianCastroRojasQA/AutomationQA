from playwright.sync_api import Page

from pages.configuracion.adquirente.base_catalogo_page import BaseCatalogoPage


class TecnologiasPage(BaseCatalogoPage):
    """
    Page Object para la sección de 'Tecnología'.
    Hereda toda la funcionalidad del catálogo base.
    """

    # ------------------------------------------------------------------
    # Constantes específicas de Tecnología
    # ------------------------------------------------------------------
    SECTION_TITLE = "Tecnología"
    INPUT_MAX_LENGTH = "50"

    WARNING_DUPLICADO_TEXT = "Existe una tecnología con ese nombre"
    ERROR_ELIMINAR_RELACION_TEXT = (
        "No es posible eliminar la Tecnología, la misma está relacionada a un Modelo de Terminal"
    )

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------
    def __init__(self, page: Page):
        super().__init__(page, logger_name="TecnologiaPage")
        self.log.debug(
            f"Cargando configuración específica para Tecnologías (ABCUC022). "
            f"MaxLen: {self.INPUT_MAX_LENGTH}"
        )

        self.log.info(
            "Contexto de 'Tecnologías' establecido. "
            "Selectores vinculados a la sección ABCUC022."
        )
