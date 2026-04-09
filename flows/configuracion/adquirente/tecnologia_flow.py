from flows.configuracion.adquirente.base_catalogo_flow import BaseCatalogoFlow
from pages.configuracion.adquirente.tecnologia_page import TecnologiaPage


class TecnologiaFlow(BaseCatalogoFlow):
    """
    Flow funcional para la pantalla de Tecnologia (ABCUC022).
    Hereda todos los flujos genéricos desde BaseCatalogoFlow.
    """

    def __init__(self, page):
        super().__init__(page, TecnologiaPage(page))
