from datetime import datetime

from core.config.settings import settings
from core.utils.sql_formatter import format_sql
from core.utils.logger import get_logger

log = get_logger("SQLEvidence")


def capturar_evidencia_sql(
    nombre_caso: str,
    nombre_paso: str,
    query: str,
    params=None,
    resultado=None
) -> None:
    """
    Genera un archivo técnico (.txt) con la trazabilidad completa de una operación en DB.

    Organización de archivos:
        EVIDENCIAS_DIR / YYYY-MM-DD / nombre_caso / SQL_HH-MM-SS_nombre_paso.txt

    Args:
        nombre_caso: Identificador del test (ej. TC-MARCAS-01).
        nombre_paso: Descripción corta del paso (ej. 01_Validacion_DB).
        query: Consulta SQL ejecutada (se formatea automáticamente).
        params: Parámetros inyectados en la consulta (lista, tupla o valor único).
        resultado: Retorno de la DB (dict, list, o None).
    """
    try:
        log.debug(f"Preparando volcado de traza SQL para el paso: {nombre_paso}...")

        # 1. Gestión de directorios dinámica
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        folder = settings.EVIDENCIAS_DIR / fecha_actual / nombre_caso
        folder.mkdir(parents=True, exist_ok=True)

        log.debug(f"Estructura de carpetas verificada en: {folder}")

        # 2. Nombre del archivo con timestamp (evita colisiones)
        ts = datetime.now().strftime("%H-%M-%S")
        path = folder / f"SQL_{ts}_{nombre_paso}.txt"

        # 3. Construcción del contenido del reporte
        contenido = [
            f"TIMESTAMP : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"PROYECTO  : {settings.PROYECTO}",
            f"AMBIENTE  : {settings.AMBIENTE}",
            f"CASO      : {nombre_caso}",
            f"PASO      : {nombre_paso}",
            "-" * 60,
            "QUERY:",
            format_sql(query),
            "",
            "PARAMS:"
        ]

        # 4. Manejo de parámetros
        if params:
            if isinstance(params, (list, tuple)):
                for p in params:
                    contenido.append(f"  - {p}")
            else:
                contenido.append(f"  - {params}")
        else:
            contenido.append("  (sin parámetros)")

        # 5. Volcado del resultado
        contenido.extend([
            "",
            "RESULTADO EN DB:",
            str(resultado) if resultado is not None else "N/A"
        ])

        # 6. Persistencia en disco
        path.write_text("\n".join(contenido), encoding="utf-8")
        log.info(f"SQL_TRACE: Evidencia técnica guardada en {path.name}")

    except Exception as e:
        log.error(
            f"ERROR DE SISTEMA: No se pudo escribir el log de SQL en disco. Error: {e}"
        )
