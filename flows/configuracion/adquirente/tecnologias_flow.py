from flows.configuracion.adquirente.base_catalogo_flow import BaseCatalogoFlow
from pages.configuracion.adquirente.tecnologias_page import TecnologiasPage
from utils.logger import get_logger


class TecnologiasFlow(BaseCatalogoFlow):
    """
    Flow funcional para la pantalla de Tecnologia (ABCUC022).
    Hereda todos los flujos genéricos desde BaseCatalogoFlow.
    """

    def __init__(self, page):
        logger = get_logger(self.__class__.__name__)
        logger.debug("Inicializando TecnologíasFlow para la pantalla ABCUC022.")

        logger.info("=== COMPONENTE: CATÁLOGO DE TECNOLOGÍAS (ABCUC022) ===")

        super().__init__(page, TecnologiasPage(page))

        logger.debug("TecnologiasPage vinculada exitosamente con el driver de Playwright.")
