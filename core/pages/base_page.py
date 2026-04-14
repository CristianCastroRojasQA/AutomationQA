from abc import ABC
from pathlib import Path
from typing import List, Optional, Union

from playwright.sync_api import Page, Locator, expect

from core.utils.logger import get_logger


class BasePage(ABC):
    """
    Abstracción base genérica para el patrón Page Object Model (POM).

    Responsabilidad ÚNICA: ser un wrapper trazable y seguro sobre la API
    de Playwright. Esta clase NO debe conocer ningún elemento, selector,
    URL ni lógica de negocio de ningún producto específico.

    Herencia esperada:
        Cada producto crea su propia BasePage que hereda de esta clase
        y agrega los elementos transversales de su aplicación.
        Ejemplo: products/paystudio/pages/base_page.py

    Attributes:
        page (Page): Instancia activa de la página de Playwright.
        log (Logger): Logger configurado con el nombre de la clase hija.
        _timeout (int): Timeout principal para esperas explícitas (ms).
        _timeout_half (int): Timeout reducido para validaciones rápidas (ms).
        _animation_wait (int): Espera para estabilización de animaciones (ms).
    """

    def __init__(self, page: Page, timeout: int, animation_wait: int, logger_name: str = "BasePage"):
        """
        Args:
            page: Instancia de Playwright Page.
            timeout: Timeout en ms para operaciones de red/URL.
            animation_wait: Espera en ms para estabilización de UI.
            logger_name: Nombre que se usará en los logs (normalmente la clase hija).
        """
        self.page = page
        self.log = get_logger(logger_name)
        self._timeout = timeout
        self._timeout_half = timeout // 2
        self._animation_wait = animation_wait

        self.log.debug(
            f"[CORE] BasePage inicializada para '{logger_name}'. "
            f"Timeout={self._timeout}ms, AnimationWait={self._animation_wait}ms"
        )

    # =========================================================================
    # ESPERAS Y VALIDACIONES DE ESTADO
    # =========================================================================

    def wait_visible(self, locator: Locator, desc: str = "elemento") -> Locator:
        """Espera y valida que un elemento sea visible antes de interactuar."""
        self.log.debug(f"[WAIT_VISIBLE] {desc}")
        expect(locator).to_be_visible(timeout=self._timeout_half)
        return locator

    def wait_hidden(self, locator: Locator, desc: str = "elemento") -> Locator:
        """Espera a que un elemento desaparezca (spinners, overlays, etc.)."""
        self.log.debug(f"[WAIT_HIDDEN] {desc}")
        expect(locator).to_be_hidden(timeout=self._timeout_half)
        return locator

    def wait_enabled(self, locator: Locator, desc: str = "elemento") -> Locator:
        """Espera a que un elemento sea interactuable (no disabled)."""
        self.log.debug(f"[WAIT_ENABLED] {desc}")
        expect(locator).to_be_enabled(timeout=self._timeout_half)
        return locator

    def wait_for_url(self, url_pattern: str):
        """Espera a que la URL actual coincida con el patrón dado."""
        self.log.debug(f"[WAIT_URL] Esperando URL que coincida con: {url_pattern}")
        self.page.wait_for_url(url_pattern, timeout=self._timeout, wait_until="networkidle")

    def wait_for_load(self, state: str = "networkidle"):
        """Espera a que la red esté estable. States: 'load', 'domcontentloaded', 'networkidle'."""
        self.log.debug(f"[WAIT_LOAD] Esperando estado de red: {state}")
        self.page.wait_for_load_state(state)

    def wait_animation(self):
        """Pausa la ejecución el tiempo configurado para estabilizar animaciones de UI."""
        self.log.debug(f"[WAIT_ANIMATION] Esperando {self._animation_wait}ms")
        self.page.wait_for_timeout(self._animation_wait)

    # =========================================================================
    # LECTURA DE ESTADO DE ELEMENTOS
    # =========================================================================

    def get_text(self, locator: Locator, desc: str = "elemento") -> str:
        """Retorna el texto visible de un elemento (inner_text limpio)."""
        self.log.debug(f"[GET_TEXT] {desc}")
        self.wait_visible(locator, desc)
        return locator.inner_text().strip()

    def get_value(self, locator: Locator, desc: str = "input") -> str:
        """Retorna el valor actual de un input/textarea."""
        self.log.debug(f"[GET_VALUE] {desc}")
        self.wait_visible(locator, desc)
        return locator.input_value()

    def get_attribute(self, locator: Locator, attribute: str, desc: str = "elemento") -> Optional[str]:
        """Retorna el valor de un atributo HTML del elemento."""
        self.log.debug(f"[GET_ATTR] {desc} -> {attribute}")
        self.wait_visible(locator, desc)
        return locator.get_attribute(attribute)

    def is_visible(self, locator: Locator) -> bool:
        """Verifica si un elemento es visible sin fallar el test."""
        return locator.is_visible()

    def is_enabled(self, locator: Locator) -> bool:
        """Verifica si un elemento es interactuable sin fallar el test."""
        return locator.is_enabled()

    def is_checked(self, locator: Locator) -> bool:
        """Verifica si un checkbox/radio está seleccionado."""
        return locator.is_checked()

    # =========================================================================
    # ACCIONES ATÓMICAS (INTERACCIONES)
    # =========================================================================

    def click(self, locator: Locator, desc: str = "elemento"):
        """Click estándar con espera de visibilidad previa."""
        self.log.info(f"[CLICK] {desc}")
        self.wait_visible(locator, desc)
        try:
            locator.click()
        except Exception as e:
            self.log.error(
                f"[CLICK_FAILED] No se pudo hacer click en '{desc}'. "
                "Posible elemento superpuesto o no interactuable."
            )
            raise e

    def click_force(self, locator: Locator, desc: str = "elemento"):
        """Click forzado cuando el elemento está cubierto por overlays."""
        self.log.info(f"[CLICK_FORCE] {desc}")
        locator.click(force=True)

    def double_click(self, locator: Locator, desc: str = "elemento"):
        """Doble click sobre un elemento."""
        self.log.info(f"[DOUBLE_CLICK] {desc}")
        self.wait_visible(locator, desc)
        locator.dblclick()

    def fill(self, locator: Locator, text: str, desc: str = "campo", mask: bool = False):
        """Limpia e ingresa texto en un input. mask=True oculta el valor en logs."""
        log_value = "***" if mask else text
        self.log.info(f"[FILL] {desc} = '{log_value}'")
        self.wait_visible(locator, desc)
        locator.fill(text)

    def type_slowly(self, locator: Locator, text: str, delay: int = 50, desc: str = "campo"):
        """Escribe texto carácter a carácter. Útil para inputs con autocomplete."""
        self.log.info(f"[TYPE] {desc} (delay={delay}ms)")
        self.wait_visible(locator, desc)
        locator.type(text, delay=delay)

    def clear(self, locator: Locator, desc: str = "campo"):
        """Limpia el contenido de un input."""
        self.log.debug(f"[CLEAR] {desc}")
        self.wait_visible(locator, desc)
        locator.clear()

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
        """Coloca el foco del teclado en el elemento."""
        self.log.debug(f"[FOCUS] {desc}")
        self.wait_visible(locator, desc)
        locator.focus()

    def press(self, locator: Locator, key: str, desc: str = "elemento"):
        """Presiona una tecla sobre el elemento (ej. 'Enter', 'Tab', 'Escape')."""
        self.log.debug(f"[PRESS] {desc} -> {key}")
        self.wait_visible(locator, desc)
        locator.press(key)

    def press_keyboard(self, key: str):
        """Presiona una tecla a nivel de página, sin foco en elemento específico."""
        self.log.debug(f"[KEYBOARD] -> {key}")
        self.page.keyboard.press(key)

    def select_option(
        self,
        locator: Locator,
        *,
        value: Optional[str] = None,
        label: Optional[str] = None,
        index: Optional[int] = None,
        desc: str = "select"
    ):
        """Selecciona una opción en un <select> HTML por valor, etiqueta o índice."""
        self.log.debug(f"[SELECT_OPTION] {desc} (value={value}, label={label}, index={index})")
        self.wait_visible(locator, desc)
        kwargs = {k: v for k, v in {"value": value, "label": label, "index": index}.items() if v is not None}
        locator.select_option(**kwargs)

    def set_input_files(
        self,
        locator: Locator,
        files: Union[str, Path, List[str], List[Path]],
        desc: str = "input file"
    ):
        """Carga uno o más archivos en un input de tipo file."""
        self.log.debug(f"[SET_FILES] {desc} -> {files}")
        self.wait_visible(locator, desc)
        locator.set_input_files(files)

    def scroll_into_view(self, locator: Locator, desc: str = "elemento"):
        """Desplaza la página hasta que el elemento sea visible en el viewport."""
        self.log.debug(f"[SCROLL_INTO_VIEW] {desc}")
        locator.scroll_into_view_if_needed()

    # =========================================================================
    # NAVEGACIÓN
    # =========================================================================

    def goto(self, url: str):
        """Navega a una URL absoluta."""
        self.log.info(f"[GOTO] {url}")
        self.page.goto(url)

    def reload(self):
        """Recarga la página actual."""
        self.log.info("[RELOAD] Recargando página...")
        self.page.reload()

    def go_back(self):
        """Navega a la página anterior del historial."""
        self.log.info("[BACK] Navegando hacia atrás...")
        self.page.go_back()

    # =========================================================================
    # UTILIDADES DE PÁGINA
    # =========================================================================

    def get_current_url(self) -> str:
        """Retorna la URL actual de la página."""
        return self.page.url

    def get_title(self) -> str:
        """Retorna el título de la página (<title>)."""
        return self.page.title()

    def take_screenshot(self, path: Union[str, Path], full_page: bool = False):
        """Toma una captura de pantalla y la guarda en la ruta indicada."""
        self.log.debug(f"[SCREENSHOT] -> {path}")
        self.page.screenshot(path=str(path), full_page=full_page)
