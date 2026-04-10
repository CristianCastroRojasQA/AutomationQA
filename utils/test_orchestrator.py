from pathlib import Path
from datetime import datetime
from logging import Logger
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import pytest

from pages.common.error_handler_page import ErrorHandlerPage
from utils.screenshots import capturar_evidencia


class TestOrchestrator:
    """
    Motor principal para la ejecución de flujos de prueba.
    Gestiona la navegación, captura de errores funcionales y técnicos, 
    y asegura que los reportes se guarden en la raíz del proyecto.
    """

    def __init__(self, page: Page, logger: Logger, test_name: str):
        self.page = page
        self.log = logger
        self.test_name = test_name
        self.errors = []
        self.omitted = []
        # FIJAMOS LA RAÍZ: Siempre en la raíz de ejecución del proyecto
        self.reports_path = Path.cwd() / "reports"

    def ejecutar_flujo(self, pasos_prueba: list):
        """
        Ejecuta una lista de pasos (tuplas de nombre y función).
        Apto para cualquier tipo de test (Smoke, Regresión, Funcional).
        """
        for nombre_paso, funcion_paso in pasos_prueba:
            self.log.info(f"--- PASO: {nombre_paso} ---")
            try:
                funcion_paso(self.test_name)
                self.log.info(f"ÉXITO: Paso '{nombre_paso}' completado.")
            except Exception as e:
                self._gestionar_error(nombre_paso, e)

        self._finalizar_ejecucion()

    def _gestionar_error(self, nombre_paso: str, error: Exception):
        """Analiza el tipo de fallo y ejecuta la acción correctiva."""
        error_msg = str(error).lower()

        # Manejo de visibilidad/timeout (Omitir si el elemento no es parte del flujo actual)
        if isinstance(error, PlaywrightTimeoutError) or ("visible" in error_msg):
            self.log.warning(f"AVISO: El paso '{nombre_paso}' no pudo completarse (No visible/Timeout).")
            self.omitted.append(nombre_paso)
            return

        # Manejo de errores de la Aplicación
        handler = ErrorHandlerPage(self.page)
        if handler.hay_error():
            detalle = handler.obtener_detalle()
            self.log.error(f"ERROR FUNCIONAL EN: {nombre_paso}")
            capturar_evidencia(self.page, self.test_name, f"ERR_FUNC_{nombre_paso}")
            self._guardar_evidencia_tecnica(nombre_paso, detalle)
            handler.aceptar_y_recuperar()
            self.errors.append(f"{nombre_paso}: Error de Aplicación")
        else:
            # Manejo de fallos técnicos de infraestructura/automatización
            self.log.error(f"FALLO TÉCNICO EN: {nombre_paso}")
            capturar_evidencia(self.page, self.test_name, f"FALLO_TECH_{nombre_paso}")
            self.page.reload()  # Intento de recuperación
            self.errors.append(f"{nombre_paso}: Fallo de Automatización")

    def _guardar_evidencia_tecnica(self, paso: str, detalle: str):
        """Guarda detalles técnicos en archivos TXT dentro de /reports/."""
        ts = datetime.now().strftime("%H%M%S")
        fecha = datetime.now().strftime("%Y-%m-%d")
        folder = self.reports_path / "error_details" / fecha / self.test_name
        folder.mkdir(parents=True, exist_ok=True)

        archivo = folder / f"DETALLE_{ts}.txt"
        archivo.write_text(f"PASO: {paso}\nHORA: {ts}\nDETALLE:\n{detalle}", encoding="utf-8")

    def _finalizar_ejecucion(self):
        """Reporta el estado final al framework de Pytest."""
        if self.errors:
            pytest.fail(f"Test finalizado con errores:\n" + "\n".join(self.errors))
