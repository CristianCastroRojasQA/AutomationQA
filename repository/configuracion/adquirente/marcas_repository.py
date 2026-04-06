from repository.base_repository import BaseRepository


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

    def obtener_marca(self, nombre: str) -> dict | None:
        query = self.SELECT_MARCA_BY_NOMBRE

        conn = self.db_manager.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (nombre,))
            row = cursor.fetchone()

            if not row:
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
