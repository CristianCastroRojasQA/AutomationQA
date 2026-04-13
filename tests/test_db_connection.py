from utils.database_manager import db_manager
from config.settings import settings
from utils.logger import get_logger

# Se utiliza el logger del proyecto para mantener un formato de salida consistente
logger = get_logger("DB_Manual_Check")


def test_manual_db_connection():
    """
    Script de diagnostico para verificar la conexion a la base de datos
    y la carga correcta de las configuraciones de entorno.
    """
    logger.info("INICIO: Diagnóstico manual de conectividad (Pre-vuelo)")
    logger.info("-" * 60)

    # 1. Diagnostico de Configuracion
    # Se listan las variables clave para confirmar que Settings leyo correctamente el entorno
    config_diagnostico = {
        "Proyecto": settings.PROYECTO,
        "Ambiente": settings.AMBIENTE,
        "Servidor": settings.DB_SERVER,
        "Base de Datos": settings.DB_NAME,
        "Usuario": settings.DB_USER
    }

    for clave, valor in config_diagnostico.items():
        logger.debug(f"Leyendo propiedad de settings: {clave} = {valor}")
        if not valor:
            logger.critical(
                f"CONFIG_MISSING: La variable '{clave}' es nula. "
                "El test fallará inevitablemente.")

            return
        else:
            logger.info(f"Configuración OK - {clave}: {valor}")

    logger.info("-" * 60)

    # 2. Ejecucion de la Validacion
    logger.info("Invocando Health Check dinámico del DatabaseManager...")
    resultado = db_manager.validar_conexion()

    # 3. Resultado Final
    if resultado:
        logger.info(
            "FIN: Infraestructura de Datos VALIDADA. "
            "Listo para ejecutar pruebas."
        )

    else:
        logger.error(
            "FALLO DE INFRAESTRUCTURA: Revise logs del DatabaseManager "
            "para detalle técnico."
        )

    logger.info("-" * 60)


if __name__ == "__main__":
    # Nota: Se recomienda ejecutar como modulo: python -m scripts.nombre_archivo
    test_manual_db_connection()
