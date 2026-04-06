from utils.logger import get_logger
from utils.sql_formatter import format_sql

logger = get_logger("Repository")

# SQL en DEBUG, no ensucia logs funcionales
logger.setLevel("DEBUG")


class BaseRepository:
    """
    Clase base para repositories.
    Logging SQL compacto: una entrada por consulta.
    """

    @staticmethod
    def log_sql(
            modulo: str,
            operacion: str,
            query: str,
            params=None,
            resultado=None
    ):
        logger.debug("")
        logger.debug("[DB][%s][%s]", modulo, operacion)
        logger.debug("---------- SQL ----------------------------------")
        logger.debug("\n%s", format_sql(query))
        logger.debug("------------------------------------------------")

        if params:
            logger.debug("Params:")
            for p in params:
                logger.debug("  - %s", p)

        if resultado:
            logger.debug("Resultado: %s", resultado)
