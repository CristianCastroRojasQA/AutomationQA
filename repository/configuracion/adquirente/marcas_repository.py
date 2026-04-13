from repository.base_repository import BaseRepository
from utils.logger import get_logger

logger = get_logger("Marcas Repository")


class MarcasRepository(BaseRepository):

    def __init__(self, db_manager, nombre_caso_prueba: str):
        self.db_manager = db_manager
        self.caso_prueba = nombre_caso_prueba

        self.TABLE_NAME = "ABC_TRADE_TECHNOLOGY"
        self.COL_ID = "ID_TRADE_TECHNOLOGY"
        self.COL_NOMBRE = "DESCRIPTION"

        self.SELECT_MARCA_BY_NOMBRE = f"""
        SELECT
            {self.COL_ID}      AS ID_MARCA,
            {self.COL_NOMBRE}  AS NOMBRE_MARCA
        FROM
            {self.TABLE_NAME}
        WHERE
            UPPER(TRIM({self.COL_NOMBRE})) = UPPER(TRIM(?))
        """

        self.SELECT_MARCA_WITH_RELATION = f"""
        SELECT DISTINCT
            M.{self.COL_ID}      AS ID_MARCA,
            M.{self.COL_NOMBRE}  AS NOMBRE_MARCA
        FROM
            {self.TABLE_NAME} M
        INNER JOIN
            ABC_MODEL_TECHNOLOGY MT
            ON MT.ID_TRADE_TECHNOLOGY = M.{self.COL_ID}
        """

    # ------------------------------------------------------------------
    # Implementación del CONTRATO del BaseRepository
    # ------------------------------------------------------------------
    def obtener_registro(self, nombre: str) -> dict | None:
        query = self.SELECT_MARCA_BY_NOMBRE
        logger.debug(f"Consultando marca '{nombre}' en tabla {self.TABLE_NAME}...")
        conn = self.db_manager.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (nombre,))
            row = cursor.fetchone()

            if not row:
                logger.warning(f"No se encontró ninguna marca coincidente con: '{nombre}'.")
                self.log_sql(
                    modulo="MARCAS",
                    operacion="SELECT",
                    query=query,
                    params=[nombre],
                    resultado="SIN_REGISTROS"
                )
                return None

            resultado = {
                "ID_MARCA": row[0],
                "NOMBRE_MARCA": str(row[1]).strip()
            }
            logger.info(
                f"Marca recuperada de la DB: {resultado['NOMBRE_MARCA']} "
                f"(ID: {resultado['ID_MARCA']})"
            )
            self.log_sql(
                modulo="MARCAS",
                operacion="SELECT",
                query=query,
                params=[nombre],
                resultado=f"REGISTRO_ENCONTRADO ID={row[0]}"
            )

            return resultado

        finally:
            cursor.close()
            conn.close()
            logger.debug("Conexión a base de datos cerrada correctamente.")

    def obtener_registro_con_relacion(self) -> dict:
        """
        Retorna una marca que tenga relación en ABC_MODEL_TECHNOLOGY,
        es decir, que NO pueda eliminarse por integridad referencial.
        """
        query = self.SELECT_MARCA_WITH_RELATION
        logger.debug("Buscando marca con integridad referencial (Join con ABC_MODEL_TECHNOLOGY)")
        conn = self.db_manager.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(query)
            row = cursor.fetchone()

            if not row:
                logger.error("Fallo de pre-condición: La base de datos no tiene marcas con modelos asociados.")
                self.log_sql(
                    modulo="MARCAS",
                    operacion="SELECT_RELACION",
                    query=query,
                    params=[],
                    resultado="SIN_REGISTROS"
                )
                raise AssertionError("No se encontró ninguna marca con relación en ABC_MODEL_TECHNOLOGY")

            resultado = {
                "ID_REGISTRO": row[0],
                "NOMBRE_REGISTRO": str(row[1]).strip(),
                "TIPO": "MARCA"
            }

            logger.info(
                f"Seleccionada marca con relación para prueba de integridad: "
                f"{resultado['NOMBRE_REGISTRO']}"
            )

            self.log_sql(
                modulo="MARCAS",
                operacion="SELECT_RELACION",
                query=self.SELECT_MARCA_WITH_RELATION,
                params=[],
                resultado=f"REGISTRO_ENCONTRADO ID={row[0]}"
            )

            return resultado

        except Exception as e:
            logger.critical(f"Error de base de datos al intentar buscar marca con relación: {e}")
            raise

        finally:
            cursor.close()
            conn.close()
            logger.debug("Conexión a base de datos cerrada correctamente.")
