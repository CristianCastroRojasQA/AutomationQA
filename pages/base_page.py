from datetime import datetime
from pathlib import Path
from typing import List, Callable, Optional, Union

from playwright.sync_api import Page, Locator, expect

from pages.common.error_handler_page import ErrorHandlerPage
from config.settings import settings
from utils.logger import get_logger
from utils.screenshots import capturar_evidencia


class BasePage:
    """
    Abstracción base para el patrón Page Object Model (POM).

    Provee un wrapper sobre la API de Playwright para garantizar que todas las
    interacciones sean trazables (logs), seguras (esperas explícitas) y
    consistentes.

    Attributes:
        page (Page): Instancia activa de la página de Playwright.
        log (Logger): Instancia de logging configurada para la clase.
    """

    def __init__(self, page: Page, logger_name: str = "BasePage"):
        self.page = page
        self.log = get_logger(logger_name)

        # Configuración de Timeouts (Centralizada en settings)
        self._url_timeout = settings.TIMEOUT
        self._title_timeout = settings.TIMEOUT / 2
        self._animation_wait = settings.ANIMATION_WAIT

        # Locators de componentes transversales (Navbar / Footer)
        self.user_welcome = page.locator("span[id$='UserWelcome']")
        self.user_dropdown = self.user_welcome.locator("xpath=ancestor::a[1]")

    # --- Métodos de Estado y Validación ---

    def wait_visible(self, locator: Locator, desc: str = "elemento") -> Locator:
        """Asegura que el elemento sea visible antes de interactuar."""
        self.log.debug(f"[WAIT_VISIBLE] {desc}")
        expect(locator).to_be_visible(timeout=self._title_timeout)
        return locator

    def wait_hidden(self, locator: Locator, desc: str = "elemento") -> Locator:
        """Espera a que un elemento desaparezca (ej. spinners, overlays)."""
        self.log.debug(f"[WAIT_HIDDEN] {desc}")
        expect(locator).to_be_hidden(timeout=self._title_timeout)
        return locator

    def get_text(self, locator: Locator, desc: str = "elemento") -> str:
        """Obtiene el contenido de texto limpio de un elemento."""
        self.log.debug(f"[GET_TEXT] {desc}")
        self.wait_visible(locator, desc)
        return locator.inner_text().strip()

    # --- Acciones Atómicas (Interacciones) ---

    def click(self, locator: Locator, desc: str = "elemento"):
        """Realiza un clic tras validar visibilidad."""
        self.log.debug(f"[CLICK] {desc}")
        self.wait_visible(locator, desc)
        locator.click()

    def fill(self, locator: Locator, text: str, desc: str = "campo", mask: bool = False):
        """Limpia e ingresa texto. Si mask=True, oculta el valor en logs."""
        log_value = "***" if mask else text
        self.log.debug(f"[FILL] {desc} = '{log_value}'")
        self.wait_visible(locator, desc)
        locator.fill(text)

    def check(self, locator: Locator, desc: str = "checkbox"):
        """Activa un checkbox o radio button."""
        self.log.debug(f"[CHECK] {desc}")
        self.wait_visible(locator, desc)
        locator.check()

    def uncheck(self, locator: Locator, desc: str = "checkbox"):
        """Desactiva un checkbox."""
        self.log.debug(f"[UNCHECK] {desc}")
        self.wait_visible(locator, desc)
        locator.uncheck()

    def hover(self, locator: Locator, desc: str = "elemento"):
        """Simula el paso del mouse sobre un elemento."""
        self.log.debug(f"[HOVER] {desc}")
        self.wait_visible(locator, desc)
        locator.hover()

    def focus(self, locator: Locator, desc: str = "elemento"):
        """Coloca el foco del sistema en el elemento."""
        self.log.debug(f"[FOCUS] {desc}")
        self.wait_visible(locator, desc)
        locator.focus()

    def press(self, locator: Locator, key: str, desc: str = "elemento"):
        """Presiona una tecla específica (ej. 'Enter', 'Tab')."""
        self.log.debug(f"[PRESS] {desc} -> {key}")
        self.wait_visible(locator, desc)
        locator.press(key)

    def select_option(self, locator: Locator, *,
                      value: Optional[str] = None,
                      label: Optional[str] = None,
                      index: Optional[int] = None,
                      desc: str = "select"):
        """Selecciona una opción en un <select> por diversos criterios."""
        self.log.debug(f"[SELECT_OPTION] {desc} (value={value}, label={label}, index={index})")
        self.wait_visible(locator, desc)

        # Construcción dinámica de argumentos de selección
        kwargs = {k: v for k, v in {"value": value, "label": label, "index": index}.items() if v is not None}
        locator.select_option(**kwargs)

    def set_input_files(self, locator: Locator, files: Union[str, Path, List[str], List[Path]],
                        desc: str = "input file"):
        """Carga archivos en un input de tipo file."""
        self.log.debug(f"[SET_INPUT_FILES] {desc} -> {files}")
        self.wait_visible(locator, desc)
        locator.set_input_files(files)

    # --- Flujos de Navegación y Usuario ---

    def abrir_menu_perfil(self):
        """Interacción con el menú desplegable del perfil de usuario."""
        self.log.info("Abriendo menú de perfil de usuario")
        self.click(self.user_dropdown, desc="Abrir menú de usuario")

    def obtener_nombre_usuario(self) -> str:
        """Retorna el nombre del usuario logueado según el Navbar."""
        return self.get_text(self.user_welcome, desc="Nombre de usuario en Navbar")

    def navegar_a_pagina_estandar(
            self,
            pasos_de_navegacion: List[Callable[[], None]],
            segmento_url_esperado: Optional[str],
            locator_titulo_pagina: Locator,
            nombre_caso_prueba: str,
            etiqueta_evidencia: str
    ) -> str:
        """
        Orquestador de navegación con validación de URL y captura de evidencia.

        Args:
            pasos_de_navegacion: Lista de acciones (clicks/hovers) para llegar al destino.
            segmento_url_esperado: Texto parcial de la URL para validar navegación.
            locator_titulo_pagina: Elemento clave que confirma la carga de la página.
            nombre_caso_prueba: Identificador del test para organización de archivos.
            etiqueta_evidencia: Sufijo para el nombre del screenshot.

        Returns:
            str: URL final alcanzada.
        """
        # Ejecución secuencial de pasos
        for paso in pasos_de_navegacion:
            paso()

        # Validación de cambio de URL
        if segmento_url_esperado:
            self.page.wait_for_url(
                f"**/{segmento_url_esperado}*",
                timeout=self._url_timeout,
                wait_until="networkidle"
            )

        # Sincronización final y evidencia
        locator_titulo_pagina.wait_for(state="visible", timeout=self._title_timeout)
        self.page.wait_for_timeout(self._animation_wait)

        capturar_evidencia(self.page, nombre_caso_prueba, f"Pantalla_{etiqueta_evidencia}")
        self.log.info(f"Navegación exitosa a {segmento_url_esperado or 'página destino'}")

        return self.page.url

    def verificar_y_manejar_error(self, nombre_ruta: str, nombre_caso_prueba: str):
        """
        Analiza si la aplicación lanzó un error controlado y genera un reporte técnico.

        Raises:
            AssertionError: Si se detecta un mensaje de error en la interfaz.
        """
        error_page = ErrorHandlerPage(self.page)

        if error_page.hay_error():
            self.log.error(f"Error detectado en pantalla durante ruta: {nombre_ruta}")

            # Gestión de directorios de evidencia
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            evidencia_dir = settings.EVIDENCIAS_DIR / fecha_hoy / nombre_caso_prueba
            evidencia_dir.mkdir(parents=True, exist_ok=True)

            detalle = error_page.obtener_detalle()
            timestamp = datetime.now().strftime("%H-%M-%S")

            # Persistencia de evidencias (Visual y Técnica)
            capturar_evidencia(self.page, nombre_caso_prueba, f"ERROR_{nombre_ruta}")

            txt_path = evidencia_dir / f"DETALLE_TECNICO_{timestamp}.txt"
            txt_path.write_text(f"Ruta: {nombre_ruta}\n\nDetalle:\n{detalle}", encoding="utf-8")

            # Intento de recuperación
            error_page.aceptar_y_recuperar()

            raise AssertionError(f"Fallo en aplicación detectado en: {nombre_ruta}. Detalles en {txt_path.name}")
