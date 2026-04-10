from repository.base_repository import BaseRepository


class TecnologiaRepository(BaseRepository):

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

        conn = self.db_manager.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (nombre,))
            row = cursor.fetchone()

            if not row:
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

            return resultado

        finally:
            cursor.close()
            conn.close()

    def obtener_registro_con_relacion(self) -> dict:
        """
        Retorna una tecnología que tenga relación en ABC_MODEL_TECHNOLOGY,
        es decir, que NO pueda eliminarse por integridad referencial.
        """
        query = self.SELECT_TECNOLOGIA_WITH_RELATION

        conn = self.db_manager.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(query)
            row = cursor.fetchone()

            if not row:
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

            self.log_sql(
                modulo="TECNOLOGIAS",
                operacion="SELECT_RELACION",
                query=query,
                params=[],
                resultado=f"REGISTRO_ENCONTRADO ID={row[0]}"
            )

            return resultado

        finally:
            cursor.close()
            conn.close()
