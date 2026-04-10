import os
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
    logger.info("-" * 60)
    logger.info("INICIANDO DIAGNOSTICO DE CONEXION A BASE DE DATOS")
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
        if not valor:
            logger.warning(f"ADVERTENCIA - {clave}: No definido en la configuracion")
        else:
            logger.info(f"Configuracion - {clave}: {valor}")

    logger.info("-" * 60)

    # 2. Ejecucion de la Validacion
    # El DatabaseManager ya gestiona internamente el cierre de la conexion
    resultado = db_manager.validar_conexion()

    # 3. Resultado Final
    if resultado:
        logger.info("RESULTADO: Conexion exitosa. El ambiente es alcanzable.")
    else:
        logger.error("RESULTADO: Error de conexion.")
        logger.error("Verificar: 1. Estado de la VPN. 2. Firewall. 3. Credenciales en .env.")

    logger.info("-" * 60)


if __name__ == "__main__":
    # Nota: Se recomienda ejecutar como modulo: python -m scripts.nombre_archivo
    test_manual_db_connection()
