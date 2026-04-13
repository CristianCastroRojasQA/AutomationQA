import pytest
from utils.screenshots import capturar_evidencia


class BugReporter:
    """
    Componente especializado en la detección y reporte de defectos funcionales (Bugs).
    Se utiliza cuando la UI responde, pero el resultado es incorrecto.
    """

    @staticmethod
    def certificar_falla(page, logger, nombre_caso, etiqueta, mensaje):
        """
        Reporta un fallo funcional con trazabilidad completa.
        """

        # CRITICAL: Inicio formal del reporte de bug
        logger.critical(f"--- INICIO REPORTE DE BUG: {etiqueta} ---")

        # ERROR: Mensaje de negocio (defecto)
        logger.error(f"🔴 DEFECTO FUNCIONAL DETECTADO: {mensaje}")
        logger.error("=" * 70)

        # DEBUG: Confirmación técnica antes de capturar evidencia
        logger.debug(f"Generando captura de pantalla de evidencia técnica para el caso: {nombre_caso}...")

        # Evidencia visual diferenciada
        capturar_evidencia(page, nombre_caso, f"DEFECTO_{etiqueta}")

        # INFO: Evidencia almacenada correctamente
        logger.info(f"Evidencia guardada exitosamente con el prefijo: DEFECTO_{etiqueta}")

        # ERROR final antes de terminar ejecución
        logger.error(f"Resumen del Defecto: {mensaje}. Terminando ejecución del test.")

        # Pytest marcará el test como FAILED (defecto de negocio)
        pytest.fail(f"Bug de Negocio: {mensaje}")
