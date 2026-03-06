# pages/base_page.py
from playwright.sync_api import Page, Locator, expect
from utils.logger import get_logger


class BasePage:
    """
    BasePage = wrapper de acciones comunes con Playwright usando Locator.
    - NO tiene selectores: los selectores viven en cada Page Object.
    - NO tiene lógica de negocio: solo acciones atómicas (click, fill, etc).
    - SI tiene logs consistentes: para trazabilidad total en la consola.
    """

    def __init__(self, page: Page, logger_name: str = "BasePage"):
        # Inicializa la página del navegador y el sistema de logs para la clase
        self.page = page
        self.log = get_logger(logger_name)

    # -------------------------
    # Helpers de espera / estado
    # -------------------------
    def wait_visible(self, el: Locator, desc: str = "elemento") -> Locator:
        """Espera a que un elemento sea visible en el DOM. Si falla, lanza un error de timeout."""
        self.log.info(f"[WAIT_VISIBLE] {desc}")
        expect(el).to_be_visible()  # Aserción nativa de Playwright con auto-espera
        return el

    def wait_hidden(self, el: Locator, desc: str = "elemento") -> Locator:
        """Espera a que un elemento desaparezca del DOM (útil para spinners o modales)."""
        self.log.info(f"[WAIT_HIDDEN] {desc}")
        expect(el).to_be_hidden()
        return el

    def get_text(self, el: Locator, desc: str = "elemento") -> str:
        """Obtiene el texto de un elemento, eliminando espacios en blanco innecesarios."""
        self.log.info(f"[GET_TEXT] {desc}")
        self.wait_visible(el, desc)  # Asegura que el texto esté ahí antes de leerlo
        return el.inner_text().strip()

    # -------------------------
    # Acciones comunes (Locator API)
    # -------------------------
    def click(self, el: Locator, desc: str = "elemento"):
        """Realiza un clic sobre un elemento previamente validado como visible."""
        self.log.info(f"[CLICK] {desc}")
        self.wait_visible(el, desc)
        el.click()

    def fill(self, el: Locator, text: str, desc: str = "campo", mask: bool = False):
        """Limpia y escribe texto en un campo. mask=True evita que el dato salga en el log."""
        shown = "***" if mask else text
        self.log.info(f"[FILL] {desc} = '{shown}'")
        self.wait_visible(el, desc)
        el.fill(text)

    def check(self, el: Locator, desc: str = "checkbox"):
        """Marca una casilla de verificación o radio button."""
        self.log.info(f"[CHECK] {desc}")
        self.wait_visible(el, desc)
        el.check()

    def uncheck(self, el: Locator, desc: str = "checkbox"):
        """Desmarca una casilla de verificación."""
        self.log.info(f"[UNCHECK] {desc}")
        self.wait_visible(el, desc)
        el.uncheck()

    def hover(self, el: Locator, desc: str = "elemento"):
        """Mueve el mouse sobre un elemento (indispensable para desplegar menús hover)."""
        self.log.info(f"[HOVER] {desc}")
        self.wait_visible(el, desc)
        el.hover()

    def focus(self, el: Locator, desc: str = "elemento"):
        """Establece el foco del teclado en el elemento indicado."""
        self.log.info(f"[FOCUS] {desc}")
        self.wait_visible(el, desc)
        el.focus()

    def press(self, el: Locator, key: str, desc: str = "elemento"):
        """Simula presionar una tecla específica (Enter, Tab, Escape, etc)."""
        self.log.info(f"[PRESS] {desc} -> {key}")
        self.wait_visible(el, desc)
        el.press(key)

    def select_option(
            self,
            el: Locator,
            *,
            value: str = None,
            label: str = None,
            index: int = None,
            desc: str = "select",
    ):
        """
        Selecciona una opción de un elemento <select> por su valor, etiqueta visible o índice.
        Se usa como: select_option(el, value="1") o select_option(el, label="Opción")
        """
        self.log.info(
            f"[SELECT_OPTION] {desc} (value={value}, label={label}, index={index})"
        )
        self.wait_visible(el, desc)
        # Diccionario dinámico para pasar solo los argumentos que no sean None
        kwargs = {}
        if value is not None:
            kwargs["value"] = value
        if label is not None:
            kwargs["label"] = label
        if index is not None:
            kwargs["index"] = index
        el.select_option(**kwargs)

    def set_input_files(self, el: Locator, files, desc: str = "input file"):
        """Carga uno o varios archivos en un input de tipo file."""
        self.log.info(f"[SET_INPUT_FILES] {desc} -> {files}")
        self.wait_visible(el, desc)
        el.set_input_files(files)
