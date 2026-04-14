from abc import ABC, abstractmethod
from utils.logger import get_logger
from utils.sql_formatter import format_sql
import time

logger = get_logger("Repository")


class BaseRepository(ABC):
    """
    Clase base para repositories.
    Define el contrato común de persistencia.
    """

    @staticmethod
    def log_sql(
            modulo: str,
            operacion: str,
            query: str,
            params=None,
            resultado=None
    ):
        logger.debug(f"Ejecutando consulta SQL en módulo: {modulo}")
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

    # ------------------------------------------------------------------
    # CONTRATO OBLIGATORIO
    # ------------------------------------------------------------------
    @abstractmethod
    def obtener_registro(self, nombre: str) -> dict | None:
        """
        Retorna el registro desde DB o None si no existe.
        """
        pass

    # ------------------------------------------------------------------
    # Lógica común de infraestructura
    # ------------------------------------------------------------------
    def esperar_no_existencia(
            self,
            nombre: str,
            timeout_segundos: int = 15,
            intervalo_segundos: float = 1.0
    ) -> bool:
        """
        Espera activa hasta que el registro deje de existir en DB.
        """

        logger.info(f"INICIO: Esperando eliminación física de '{nombre}' en la base de datos...")

        inicio = time.time()

        while time.time() - inicio < timeout_segundos:
            logger.debug(
                f"Reintentando verificación de existencia para '{nombre}'... "
                f"(Tiempo transcurrido: {round(time.time() - inicio, 1)}s)"
            )
            if not self.obtener_registro(nombre):
                logger.info(f"FIN: Registro '{nombre}' ya no existe en la base de datos.")

                return True
            time.sleep(intervalo_segundos)
        logger.warning(
            f"El registro '{nombre}' sigue presente tras {timeout_segundos}s. "
            "Es posible que el borrado haya fallado o sea lento."
        )
        return False
