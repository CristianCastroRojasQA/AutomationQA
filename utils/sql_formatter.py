import textwrap


def format_sql(query: str) -> str:
    """
    Normaliza el SQL eliminando indentación innecesaria,
    preservando saltos de línea y formato semántico.
    """
    return textwrap.dedent(query).strip()
