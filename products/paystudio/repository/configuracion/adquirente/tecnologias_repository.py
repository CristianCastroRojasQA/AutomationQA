from products.paystudio.repository.base_repository import BaseRepository
from core.utils.logger import get_logger

logger = get_logger("Tecnologías Repository")


class TecnologiasRepository(BaseRepository):

    def __init__(self, db_manager, nombre_caso_prueba: str):
        self.db_manager = db_manager
        self.caso_prueba = nombre_caso_prueba

        self.TABLE_NAME = "ABC_TERM_TECH_COMMUNICATION"
        self.COL_ID = "ID_TERM_TECH_COMMUNICATION"
        self.COL_NOMBRE = "DESCRIPTION"

        self.SELECT_TECNOLOGIA_BY_NOMBRE = f"""
        SELECT
            {self.COL_ID}      AS ID_TECNOLOGIA,
            {self.COL_NOMBRE}  AS NOMBRE_TECNOLOGIA
        FROM
            {self.TABLE_NAME}
        WHERE
            UPPER(TRIM({self.COL_NOMBRE})) = UPPER(TRIM(?))
        """

        self.SELECT_TECNOLOGIA_WITH_RELATION = f"""
        SELECT DISTINCT
            T.{self.COL_ID}     AS ID_TECNOLOGIA,
            T.{self.COL_NOMBRE} AS NOMBRE_TECNOLOGIA
        FROM
            {self.TABLE_NAME} T
        INNER JOIN
            ABC_MODEL_TECHNOLOGY MT
            ON MT.ID_TERM_TECH_COMMUNICATION = T.{self.COL_ID}
        """

    # ------------------------------------------------------------------
    # Implementación del CONTRATO del BaseRepository
    # ------------------------------------------------------------------
    def obtener_registro(self, nombre: str) -> dict | None:
        query = self.SELECT_TECNOLOGIA_BY_NOMBRE
        logger.debug(f"Consultando tecnología '{nombre}' en tabla {self.TABLE_NAME}...")
        conn = self.db_manager.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (nombre,))
            row = cursor.fetchone()

            if not row:
                logger.warning(f"No se encontró información para la tecnología: '{nombre}'.")
                self.log_sql(
                    modulo="TECNOLOGIA",
                    operacion="SELECT",
                    query=query,
                    params=[nombre],
                    resultado="SIN_REGISTROS"
                )
                return None

            resultado = {
                "ID_TECNOLOGIA": row[0],
                "NOMBRE_TECNOLOGIA": str(row[1]).strip()
            }

            self.log_sql(
                modulo="TECNOLOGIA",
                operacion="SELECT",
                query=query,
                params=[nombre],
                resultado=f"REGISTRO_ENCONTRADO ID={row[0]}"
            )
            logger.info(
                f"Tecnología recuperada de DB: {resultado['NOMBRE_TECNOLOGIA']} "
                f"(ID: {resultado['ID_TECNOLOGIA']})"
            )

            return resultado

        finally:
            cursor.close()
            conn.close()
            logger.debug("Cerrando conexión de base de datos para el módulo TECNOLOGIA.")

    def obtener_registro_con_relacion(self) -> dict:
        """
        Retorna una tecnología que tenga relación en ABC_MODEL_TECHNOLOGY,
        es decir, que NO pueda eliminarse por integridad referencial.
        """
        query = self.SELECT_TECNOLOGIA_WITH_RELATION
        logger.debug("Buscando tecnología con integridad referencial (Join con ABC_MODEL_TECHNOLOGY)")
        conn = self.db_manager.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(query)
            row = cursor.fetchone()

            if not row:
                logger.error("Fallo de pre-condición: La base de datos no tiene tecnologías con modelos asociados.")
                self.log_sql(
                    modulo="TECNOLOGIAS",
                    operacion="SELECT_RELACION",
                    query=query,
                    params=[],
                    resultado="SIN_REGISTROS"
                )
                raise AssertionError(
                    "No se encontró ninguna tecnología con relación en ABC_MODEL_TECHNOLOGY"
                )

            resultado = {
                "ID_REGISTRO": row[0],
                "NOMBRE_REGISTRO": str(row[1]).strip(),
                "TIPO": "TECNOLOGIA"
            }
            logger.info(
                f"Seleccionada tecnología con relación para prueba de integridad: "
                f"{resultado['NOMBRE_REGISTRO']}"
            )

            self.log_sql(
                modulo="TECNOLOGIAS",
                operacion="SELECT_RELACION",
                query=query,
                params=[],
                resultado=f"REGISTRO_ENCONTRADO ID={row[0]}"
            )

            return resultado
        except Exception as e:
            logger.critical(f"Error de base de datos al intentar buscar tecnología con relación: {e}")
            raise

        finally:
            cursor.close()
            conn.close()
            logger.debug("Cerrando conexión de base de datos para el módulo TECNOLOGIA.")
