from playwright.sync_api import Page

from pages.configuracion.adquirente.base_catalogo_page import BaseCatalogoPage


class TecnologiaPage(BaseCatalogoPage):
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
