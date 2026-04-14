import textwrap

from core.utils.logger import get_logger

log = get_logger("SQLFormatter")


def format_sql(query: str) -> str:
    """
    Limpia y normaliza el formato de una consulta SQL para legibilidad en reportes.

    - Elimina indentación relativa (textwrap.dedent).
    - Elimina espacios/saltos de línea al inicio y fin.

    Args:
        query: String con la consulta SQL a formatear.

    Returns:
        str: Query normalizada o 'QUERY VACIA' si el input es nulo/vacío.
    """
    if not query:
        log.warning("Se intentó formatear una cadena SQL vacía o None.")
        return "QUERY VACIA"

    sql_normalizado = textwrap.dedent(query).strip()

    log.debug(f"SQL normalizado exitosamente ({len(query)} caracteres).")

    return sql_normalizado
