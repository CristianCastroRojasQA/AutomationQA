import textwrap


def format_sql(query: str) -> str:
    """
    Limpia y normaliza el formato de una consulta SQL para su lectura.
    """
    if not query:
        return "QUERY VACIA"
    # Eliminamos espacios en blanco innecesarios en los extremos y dedentamos
    return textwrap.dedent(query).strip()
