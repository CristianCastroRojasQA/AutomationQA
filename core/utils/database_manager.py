import pyodbc

from core.config.settings import settings
from core.utils.logger import get_logger

logger = get_logger("DatabaseManager")


class DatabaseManager:
    """
    Gestiona la conectividad con SQL Server vía pyodbc.

    Responsabilidad: establecer conexiones y realizar health checks.
    Es agnóstico al producto — las credenciales vienen de settings (cargadas del .env).

    Uso:
        from core.utils.database_manager import db_manager
        ok = db_manager.validar_conexion()
    """

    def __init__(self):
        """Inicializa parámetros de conexión desde la configuración global."""
        self.server   = settings.DB_SERVER
        self.database = settings.DB_NAME
        self.username = settings.DB_USER
        self.password = settings.DB_PASS
        self.driver   = "{SQL Server}"

    def conectar(self):
        """
        Crea y retorna un objeto de conexión pyodbc.

        Returns:
            pyodbc.Connection | None: Conexión activa, o None si falla.
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
                f"FALLO DE RED/ACCESO: No se puede alcanzar {self.server}. Error: {e}"
            )
            return None

    def validar_conexion(self) -> bool:
        """
        Health Check de la base de datos. Ejecuta SELECT GETDATE().

        Returns:
            bool: True si la conexión y la consulta son exitosas, False si no.
        """
        logger.info(f"INICIO: Health check de base de datos en: {self.database}")

        conexion = self.conectar()

        if conexion is None:
            logger.error(
                f"La conexión retornó None. Revise credenciales del usuario: {self.username}"
            )
            return False

        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT GETDATE()")
                    row = cursor.fetchone()

                    if row:
                        logger.info(
                            f"FIN: Conexión validada. Sync con DB exitosa (Fecha: {row[0]})"
                        )
                        return True
                    else:
                        logger.warning(
                            "Consulta GETDATE() no retornó datos. "
                            "El servidor responde pero la sesión es inestable."
                        )
                        return False

        except Exception as e:
            logger.error(f"Error de ejecución en Health Check: {e}")
            return False
        finally:
            try:
                conexion.close()
            except Exception:
                pass
            logger.debug("Recursos de conexión liberados en DatabaseManager.")


# Instancia global — importar como: from core.utils.database_manager import db_manager
db_manager = DatabaseManager()
