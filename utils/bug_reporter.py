import pytest
from utils.screenshots import capturar_evidencia


class BugReporter:
    """
    Componente especializado en la detección y reporte de defectos funcionales (Bugs).
    A diferencia de ErrorHandler, este se usa cuando la UI responde pero el resultado es incorrecto.
    """

    @staticmethod
    def certificar_falla(page, logger, nombre_caso, etiqueta, mensaje):
        """
        Reporta un fallo funcional con trazabilidad completa.
        """
        logger.error("=" * 70)
        logger.error(f"🔴 DEFECTO FUNCIONAL DETECTADO: {mensaje}")
        logger.error("=" * 70)

        # Evidencia con prefijo de BUG para diferenciar de fotos de flujo normal
        capturar_evidencia(page, nombre_caso, f"DEFECTO_{etiqueta}")

        # Pytest marcará el test como FAILED (no como ERROR técnico)
        pytest.fail(f"Bug de Negocio: {mensaje}")
