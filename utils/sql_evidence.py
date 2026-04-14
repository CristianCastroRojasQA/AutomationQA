from datetime import datetime
from config.settings import settings  # Importación de rutas y entorno centralizado
from utils.sql_formatter import format_sql
from utils.logger import get_logger

# Instancia del logger específica para el rastreo de SQL
log = get_logger("SQLEvidence")


def capturar_evidencia_sql(nombre_caso: str, nombre_paso: str, query: str, params=None, resultado=None):
    """
    Genera un archivo técnico (.txt) con la trazabilidad completa de una operación en base de datos.

    Argumentos:
        nombre_caso (str): Identificador del caso de prueba (ej: TC-MARCAS-01).
        nombre_paso (str): Descripción corta del paso (ej: 01_Validacion_DB).
        query (str): La consulta SQL ejecutada (será formateada automáticamente).
        params (list/tuple, opcional): Parámetros inyectados en la consulta.
        resultado (any, opcional): El retorno de la base de datos (dict, list o None).
    """
    try:
        log.debug(f"Preparando volcado de traza SQL para el paso: {nombre_paso}...")

        # 1. GESTIÓN DE DIRECTORIOS DINÁMICA
        # Se utiliza settings.EVIDENCIAS_DIR definido en el .env para evitar rutas relativas rotas.
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        folder = settings.EVIDENCIAS_DIR / fecha_actual / nombre_caso
        folder.mkdir(parents=True, exist_ok=True)

        log.debug(f"Estructura de carpetas verificada en: {folder}")

        # 2. CONSTRUCCIÓN DEL NOMBRE DEL ARCHIVO
        # Incluimos timestamp para evitar colisiones si se ejecuta la misma query varias veces.
        ts = datetime.now().strftime("%H-%M-%S")
        path = folder / f"SQL_{ts}_{nombre_paso}.txt"

        # 3. PREPARACIÓN DEL CONTENIDO
        # Formateamos el encabezado con datos del entorno para mayor trazabilidad en auditorías.
        contenido = [
            f"TIMESTAMP : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"PROYECTO  : {settings.PROYECTO}",
            f"AMBIENTE  : {settings.AMBIENTE}",
            f"CASO      : {nombre_caso}",
            f"PASO      : {nombre_paso}",
            "-" * 60,
            "QUERY:",
            format_sql(query),  # Limpia indentación y normaliza el SQL
            "",
            "PARAMS:"
        ]

        # Manejo dinámico de parámetros de entrada
        if params:
            # Si params es una lista/tupla, se desglosa línea por línea
            if isinstance(params, (list, tuple)):
                for p in params: contenido.append(f"  - {p}")
            else:
                contenido.append(f"  - {params}")
        else:
            contenido.append("  (sin parámetros)")

        # 4. VOLCADO DE RESULTADOS REALES
        # Se convierte el objeto resultado (diccionario o lista) a string.
        # Esto permite ver en el TXT exactamente lo que devolvió el motor de DB.
        contenido.extend([
            "",
            "RESULTADO EN DB:",
            str(resultado) if resultado is not None else "N/A"
        ])

        # 5. PERSISTENCIA
        path.write_text("\n".join(contenido), encoding="utf-8")

        # Log en nivel INFO para confirmar la creación del artefacto
        log.info(f"SQL_TRACE: Evidencia técnica guardada en {path.name}")


    except Exception as e:
        # Captura cualquier error de permisos o escritura para no detener el flujo del test
        log.error(
            f"ERROR DE SISTEMA: No se pudo escribir el log de SQL en disco. "
            f"Error: {e}"
        )
