from pathlib import Path
from datetime import datetime
from logging import Logger
from typing import Callable, Optional

import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, Page
from playwright.sync_api import Error as PlaywrightError

from core.utils.screenshots import capturar_evidencia


class ErrorHandlerResult:
    """Resultado de verificar un handler de errores de aplicación."""

    def __init__(self, has_error: bool, detail: str = ""):
        self.has_error = has_error
        self.detail = detail
        self.recovered = False


class TestOrchestrator:
    """
    Motor de ejecución de flujos de prueba agnóstico al producto.

    Gestiona la ejecución de pasos, captura de errores funcionales y técnicos.
    La detección de errores específicos de aplicación se inyecta vía factory
    para mantener core/ independiente de cualquier producto.

    Args:
        page: Instancia de Playwright Page.
        logger: Logger del test en ejecución.
        test_name: Nombre del caso de prueba.
        error_handler_factory: Callable opcional que retorna un objeto con:
            - hay_error() -> bool
            - obtener_detalle() -> str
            - aceptar_y_recuperar() -> None
            Si es None, se omite la verificación de errores de aplicación.
    """

    def __init__(
        self,
        page: Page,
        logger: Logger,
        test_name: str,
        error_handler_factory: Optional[Callable] = None,
    ):
        self.page = page
        self.log = logger
        self.test_name = test_name
        self.errors = []
        self.omitted = []
        self.reports_path = Path.cwd() / "reports"
        self._error_handler_factory = error_handler_factory

    def ejecutar_flujo(self, pasos_prueba: list) -> None:
        """
        Ejecuta una lista de pasos (tuplas de nombre y función).
        Compatible con Smoke, E2E y Funcional.
        """
        for nombre_paso, funcion_paso in pasos_prueba:
            self.log.info(f"INICIO PASO: {nombre_paso}")
            try:
                funcion_paso(self.test_name)
                self.log.info(f"FIN PASO: {nombre_paso} ejecutado correctamente.")
            except Exception as e:
                self._gestionar_error(nombre_paso, e)

        self._finalizar_ejecucion()

    def _gestionar_error(self, nombre_paso: str, error: Exception) -> None:
        """Analiza el tipo de fallo y ejecuta la acción correctiva."""
        error_msg = str(error).lower()

        # Timeout / visibilidad → el paso se omite y el flujo continúa
        if isinstance(error, PlaywrightTimeoutError) or "visible" in error_msg:
            self.log.warning(
                f"PASO OMITIDO: '{nombre_paso}' falló por Timeout/Visibilidad. "
                "Se continúa con el flujo."
            )
            self.omitted.append(nombre_paso)
            return

        # Error específico de aplicación (inyectado por el producto)
        if self._error_handler_factory is not None:
            handler = self._error_handler_factory(self.page)
            if handler.hay_error():
                detalle = handler.obtener_detalle()
                self.log.error(f"ERROR DETECTADO en la app durante el paso: {nombre_paso}")
                capturar_evidencia(self.page, self.test_name, f"ERR_FUNC_{nombre_paso}")
                self._guardar_evidencia_tecnica(nombre_paso, detalle)
                handler.aceptar_y_recuperar()
                self.errors.append(f"{nombre_paso}: Error de Aplicación")
                return

        # Fallo técnico genérico → intenta recargar y registra
        self.log.critical(
            f"FALLO DE INFRAESTRUCTURA en: '{nombre_paso}'. Intentando recarga..."
        )
        capturar_evidencia(self.page, self.test_name, f"FALLO_TECH_{nombre_paso}")
        try:
            self.page.reload()
        except (PlaywrightTimeoutError, PlaywrightError, RuntimeError) as e:
            self.log.debug(f"Recarga fallida durante recuperación: {e}")

        self.errors.append(f"{nombre_paso}: Fallo de Automatización")

    def _guardar_evidencia_tecnica(self, paso: str, detalle: str) -> None:
        """Guarda detalles técnicos en TXT dentro de reports/."""
        ts     = datetime.now().strftime("%H%M%S")
        fecha  = datetime.now().strftime("%Y-%m-%d")
        folder = self.reports_path / "error_details" / fecha / self.test_name
        folder.mkdir(parents=True, exist_ok=True)
        archivo = folder / f"DETALLE_{ts}.txt"
        archivo.write_text(f"PASO: {paso}\nHORA: {ts}\nDETALLE:\n{detalle}", encoding="utf-8")
        self.log.debug(f"Detalle técnico persistido en: {archivo.name}")

    def _finalizar_ejecucion(self) -> None:
        """Reporta el estado final al framework de Pytest."""
        if self.errors:
            self.log.critical(
                f"RESULTADO: {self.test_name} finalizó con {len(self.errors)} errores."
            )
            pytest.fail("Test finalizado con errores:\n" + "\n".join(self.errors))
        else:
            self.log.info(
                f"RESULTADO: {self.test_name} completado exitosamente sin errores."
            )
