import pytest
from logging import Logger

from core.utils.screenshots import capturar_evidencia


class BugReporter:
    """
    Componente especializado en la detección y reporte de defectos funcionales.

    Se utiliza cuando la UI de PayStudio responde correctamente pero el resultado
    de negocio es incorrecto (bug funcional, no de infraestructura).
    """

    @staticmethod
    def certificar_falla(page, logger: Logger, nombre_caso: str, etiqueta: str, mensaje: str):
        """
        Reporta un fallo funcional con trazabilidad completa.

        Args:
            page: Instancia activa de Playwright Page.
            logger: Logger del test en ejecución.
            nombre_caso: Identificador del test (para carpeta de evidencias).
            etiqueta: Sufijo para el nombre del screenshot.
            mensaje: Descripción del defecto encontrado.
        """
        logger.critical(f"--- INICIO REPORTE DE BUG: {etiqueta} ---")
        logger.error(f"🔴 DEFECTO FUNCIONAL DETECTADO: {mensaje}")
        logger.error("=" * 70)
        logger.debug(f"Generando captura de evidencia técnica para: {nombre_caso}...")

        capturar_evidencia(page, nombre_caso, f"DEFECTO_{etiqueta}")

        logger.info(f"Evidencia guardada con el prefijo: DEFECTO_{etiqueta}")
        logger.error(f"Resumen del Defecto: {mensaje}. Terminando ejecución del test.")

        pytest.fail(f"Bug de Negocio: {mensaje}")
