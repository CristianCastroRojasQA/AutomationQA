import pyodbc
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("DatabaseManager")


class DatabaseManager:
    def __init__(self):
        self.server = settings.DB_SERVER
        self.database = settings.DB_NAME
        self.username = settings.DB_USER
        self.password = settings.DB_PASS
        self.conn = None

    def conectar(self):
        """Establece la conexión a la base de datos dinámicamente."""
        try:
            # Cadena de conexión estándar para SQL Server
            conn_str = (
                f"DRIVER={{SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
                "Connection Timeout=10;"
            )
            self.conn = pyodbc.connect(conn_str)
            return self.conn
        except Exception as e:
            logger.error(f"❌ Error al conectar a la DB {self.database} en {self.server}: {e}")
            return None

    def validar_conexion(self):
        """Verifica si la base de datos responde (Health Check)."""
        logger.info(f"Intentando validar conexión dinámica a: {self.database}...")
        conexion = self.conectar()

        if conexion:
            try:
                cursor = conexion.cursor()
                # Ejecutamos una consulta simple para validar
                cursor.execute("SELECT GETDATE()")
                fecha_db = cursor.fetchone()[0]
                logger.info(f"✅ Conexión EXITOSA. Fecha servidor DB: {fecha_db}")
                cursor.close()
                conexion.close()
                return True
            except Exception as e:
                logger.error(f"❌ La conexión se estableció pero la consulta falló: {e}")
                return False
        else:
            return False


# Instancia lista para usar
db_manager = DatabaseManager()
