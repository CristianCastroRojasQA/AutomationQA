from playwright.sync_api import Page
from core.utils.logger import get_logger


class ErrorHandlerPage:
    """
    Componente de soporte para la gestión de excepciones de UI (ErrorHandlerControl).

    Detecta, extrae y gestiona las pantallas de error críticas del sistema, 
    permitiendo la recuperación del flujo o la documentación de fallos técnicos.
    """

    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger("ErrorHandler")

        # Selectores técnicos del control de errores de PayStudio
        self._lbl_titulo = page.locator("#ctl00_ContentPlaceHolder1_ErrorHandlerControl1_LabelTitle")
        self._lbl_detalle = page.locator("#ctl00_ContentPlaceHolder1_ErrorHandlerControl1_errorDetail")
        self._btn_ok = page.locator("#ctl00_ContentPlaceHolder1_ErrorHandlerControl1_ButtonOk")

    def hay_error(self) -> bool:
        """
        Verifica la presencia de la pantalla de error en el DOM actual.

        Usa un timeout reducido para no penalizar el performance de las 
        validaciones negativas durante la ejecución normal.
        """
        try:
            # DEBUG: No queremos un log cada vez que chequeamos errores en una navegación exitosa.
            is_present = self._lbl_titulo.is_visible(timeout=1500)
            if is_present:
                self.log.error(
                    f"CRITICAL UI ERROR: Se ha disparado el ErrorHandlerControl. "
                    f"Título: '{self._lbl_titulo.inner_text()}'"
                )
            return is_present
        except Exception as e:
            self.log.debug(f"Performance Trace: Timeout de 1500ms agotado sin detectar pantalla de error. {e}")
            return False

    def obtener_detalle(self) -> str:
        """
        Captura el StackTrace o mensaje técnico de la excepción.
        """
        try:
            if self._lbl_detalle.is_visible(timeout=500):
                detalle = self._lbl_detalle.inner_text().strip()
                self.log.debug(f"StackTrace Completo capturado para auditoría: {detalle}")
                return detalle
        except Exception as e:
            self.log.debug(f"Fallo al extraer metadatos del error: {e}")

        return "No se pudo extraer el detalle técnico del error."

    def aceptar_y_recuperar(self) -> None:
        """
        Intenta cerrar el diálogo de error y restablecer el estado de la página.
        """
        self.log.info("Intentando recuperar sesión tras error de sistema. Redireccionando...")
        self._btn_ok.click()
        self.log.warning("El botón 'Aceptar' del ErrorHandler fue presionado. Estado de la aplicación: Inestable.")
        # DEBUG: Espera técnica de red.
        self.log.debug("Esperando estabilización de red post-recuperación...")
        self.page.wait_for_load_state("networkidle")
