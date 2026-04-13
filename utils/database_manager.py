import pyodbc
from config.settings import settings
from utils.logger import get_logger

# Configuración del logger para el módulo de Base de Datos
logger = get_logger("DatabaseManager")


class DatabaseManager:
    """
    Clase encargada de gestionar la conectividad con SQL Server.
    Proporciona métodos para establecer conexiones y realizar verificaciones de salud (Health Checks).
    """

    def __init__(self):
        """Inicializa los parámetros de conexión basados en la configuración global."""
        self.server = settings.DB_SERVER
        self.database = settings.DB_NAME
        self.username = settings.DB_USER
        self.password = settings.DB_PASS
        self.driver = "{SQL Server}"

    def conectar(self):
        """
        Crea y retorna un objeto de conexión pyodbc.
        Returns:
            pyodbc.Connection: Objeto de conexión si es exitoso, None si falla.
        """
        logger.debug(f"Estableciendo conexión pyodbc a {self.server} (DB: {self.database})...")
        try:
            conn_str = (
                f"DRIVER={self.driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
                "Connection Timeout=10;"
            )
            return pyodbc.connect(conn_str)
        except Exception as e:
            logger.critical(
                f"FALLO DE RED/ACCESO: No se puede alcanzar el servidor "
                f"{self.server}. Error: {e}"
            )
            return None

    def validar_conexion(self):
        """
        Realiza un Health Check de la base de datos ejecutando una consulta simple.
        evitando warnings de tipos (NoneType) y fugas de recursos.
        Returns:
            bool: True si la conexión y la consulta fueron exitosas, False de lo contrario.
        """
        logger.info(f"INICIO: Health check de base de datos en: {self.database}")

        # Obtenemos la conexión
        conexion = self.conectar()

        # Validación 1: Verificar que la conexión no sea None para evitar warnings de ContextManager
        if conexion is None:
            logger.error(
                f"La conexión retornó None. Revise credenciales para el usuario: "
                f"{self.username}"
            )
            return False

        try:
            # 'with conexion' asegura el commit/rollback y 'with conexion.cursor()' asegura el cierre del cursor
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT GETDATE()")
                    row = cursor.fetchone()

                    # Validación 2: Verificar que la fila no sea None antes de acceder al índice
                    if row:
                        fecha_db = row[0]
                        logger.info(
                            f"FIN: Conexión validada. Sync con DB exitosa "
                            f"(Fecha: {fecha_db})"
                        )
                        return True
                    else:
                        # ⚠️ Caso raro: conexión existe pero sin datos
                        logger.warning(
                            "Consulta GETDATE() no retornó datos. "
                            "El servidor responde pero la sesión es inestable."
                        )
                        return False

        except Exception as e:
            logger.error(f"Error de ejecución en Health Check: {e}")
            return False
        finally:
            # Aseguramos el cierre manual de la conexión por si el context manager no lo hizo en el fallo
            try:
                conexion.close()
            except:
                pass
            logger.debug("Recursos de conexión liberados manualmente en DatabaseManager.")


# Instancia global lista para ser utilizada en fixtures o tests
db_manager = DatabaseManager()
