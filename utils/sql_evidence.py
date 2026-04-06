from pathlib import Path
from datetime import datetime
from utils.sql_formatter import format_sql
from utils.logger import get_logger

log = get_logger("SQLEvidence")


def capturar_evidencia_sql(
        nombre_caso: str,
        nombre_paso: str,
        query: str,
        params=None,
        resultado=None
):
    try:
        root_dir = Path(__file__).resolve().parent.parent
        base_dir = root_dir / "screenshots"
        fecha = datetime.now().strftime("%Y-%m-%d")
        folder = base_dir / fecha / nombre_caso
        folder.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%H-%M-%S")
        path = folder / f"{ts}_{nombre_paso}.txt"

        contenido = [
            f"TIMESTAMP : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"CASO      : {nombre_caso}",
            f"OPERACION : SQL",
            "",
            "QUERY:",
            format_sql(query),
            "",
            "PARAMS:"
        ]

        if params:
            for p in params:
                contenido.append(f"  - {p}")
        else:
            contenido.append("  (sin parámetros)")

        contenido.extend([
            "",
            "RESULTADO:",
            resultado if resultado else "N/A"
        ])

        path.write_text("\n".join(contenido), encoding="utf-8")
        log.info(f"Evidencia SQL guardada en: {path}")

    except Exception as e:
        log.error(f"Error al guardar evidencia SQL: {e}")
