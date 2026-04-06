from utils.logger import get_logger

logger = get_logger("MarcasRepository")


class MarcasRepository:

    def __init__(self, db_manager):
        self.db_manager = db_manager
        # Configuración de tabla y columnas según el modelo del sistema
        self.TABLE_NAME = "ABC_TRADE_TECHNOLOGY"
        self.COL_ID = "ID_TRADE_TECHNOLOGY"
        self.COL_NOMBRE = "DESCRIPTION"

    def obtener_marca(self, nombre: str) -> dict | None:
        """
        Consulta la base de datos para obtener los detalles de una marca por su nombre.
        Se utiliza para validar tanto la creación exitosa como la eliminación lógica/física.
        """
        query = f"""
        SELECT {self.COL_ID}, {self.COL_NOMBRE}
        FROM {self.TABLE_NAME}
        WHERE UPPER(LTRIM(RTRIM({self.COL_NOMBRE}))) = UPPER(LTRIM(RTRIM(?)))
        """

        conn = self.db_manager.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(query, (nombre,))
            row = cursor.fetchone()

            if not row:
                return None

            return {
                "ID_MARCA": row[0],
                "NOMBRE_MARCA": str(row[1]).strip() if row[1] else ""
            }
        except Exception as e:
            logger.error(f"Error al consultar marca '{nombre}': {e}")
            return None
        finally:
            cursor.close()
            conn.close()
