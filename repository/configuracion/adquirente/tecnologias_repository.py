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
