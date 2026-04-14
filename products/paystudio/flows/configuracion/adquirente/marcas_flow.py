from products.paystudio.flows.configuracion.adquirente.base_catalogo_flow import BaseCatalogoFlow
from products.paystudio.pages.configuracion.adquirente.marcas_page import MarcasPage
from core.utils.logger import get_logger


class MarcasFlow(BaseCatalogoFlow):
    """
    Flow funcional para la pantalla de Marcas (ABCUC022).
    Hereda todos los flujos genéricos desde BaseCatalogoFlow.
    """

    def __init__(self, page):
        logger = get_logger(self.__class__.__name__)

        logger.debug("Inicializando MarcasFlow para la pantalla ABCUC022.")

        super().__init__(page, MarcasPage(page))

        logger.info("=== COMPONENTE: CATÁLOGO DE MARCAS (ABCUC022) ===")

        logger.debug("MarcasPage vinculada exitosamente con el driver de Playwright.")
