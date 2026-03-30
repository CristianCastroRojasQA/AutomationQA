from utils.logger import get_logger


class ErrorHandlerPage:
    """
    Maneja la página estándar de errores de PayStudio (ErrorHandlerControl).
    """

    def __init__(self, page):
        self.page = page
        self.log = get_logger("ErrorHandler")

        # Selectores por ID estándar de la app
        self.lbl_titulo = page.locator("#ctl00_ContentPlaceHolder1_ErrorHandlerControl1_LabelTitle")
        self.lbl_detalle = page.locator("#ctl00_ContentPlaceHolder1_ErrorHandlerControl1_errorDetail")
        self.btn_ok = page.locator("#ctl00_ContentPlaceHolder1_ErrorHandlerControl1_ButtonOk")

    def hay_error(self) -> bool:
        """Verifica rápidamente si la página de error está visible."""
        try:
            # Timeout corto para no retrasar la navegación normal
            return self.lbl_titulo.is_visible(timeout=1500)
        except Exception as e:
            self.log.debug(f"Error silencioso al chequear pantalla de error: {e}")
            return False

    def obtener_detalle(self) -> str:
        """Extrae el stack trace o detalle técnico del error."""
        try:
            if self.lbl_detalle.is_visible(timeout=500):
                return self.lbl_detalle.inner_text().strip()
        except Exception as e:
            self.log.debug(f"No se pudo extraer detalle técnico: {e}")
        return "No se pudo extraer el detalle técnico del error."

    def aceptar_y_recuperar(self):
        """Presiona OK para intentar volver al estado anterior."""
        self.log.warning("Intentando recuperación: Presionando 'Aceptar' en página de error.")
        self.btn_ok.click()
        self.page.wait_for_load_state("networkidle")
