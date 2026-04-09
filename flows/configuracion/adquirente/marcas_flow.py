from flows.configuracion.adquirente.base_catalogo_flow import BaseCatalogoFlow
from pages.configuracion.adquirente.marcas_page import MarcasPage


class MarcasFlow(BaseCatalogoFlow):
    """
    Flow funcional para la pantalla de Marcas (ABCUC022).
    Hereda todos los flujos genéricos desde BaseCatalogoFlow.
    """

    def __init__(self, page):
        super().__init__(page, MarcasPage(page))
