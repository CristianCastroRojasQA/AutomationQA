# pages/base_page.py
from playwright.sync_api import Page, Locator, expect
from utils.logger import get_logger


class BasePage:
    """
    BasePage = wrapper de acciones comunes con Playwright usando Locator.
    - NO tiene selectores.
    - NO tiene lógica de negocio.
    - SI tiene logs consistentes.
    """

    def __init__(self, page: Page, logger_name: str = "BasePage"):
        self.page = page
        self.log = get_logger(logger_name)

    # -------------------------
    # Helpers de espera / estado
    # -------------------------
    def wait_visible(self, el: Locator, desc: str = "elemento") -> Locator:
        self.log.info(f"[WAIT_VISIBLE] {desc}")
        expect(el).to_be_visible()
        return el

    def wait_hidden(self, el: Locator, desc: str = "elemento") -> Locator:
        self.log.info(f"[WAIT_HIDDEN] {desc}")
        expect(el).to_be_hidden()
        return el

    def get_text(self, el: Locator, desc: str = "elemento") -> str:
        self.log.info(f"[GET_TEXT] {desc}")
        self.wait_visible(el, desc)
        return el.inner_text().strip()

    # -------------------------
    # Acciones comunes (Locator API)
    # -------------------------
    def click(self, el: Locator, desc: str = "elemento"):
        self.log.info(f"[CLICK] {desc}")
        self.wait_visible(el, desc)
        el.click()

    def fill(self, el: Locator, text: str, desc: str = "campo", mask: bool = False):
        shown = "***" if mask else text
        self.log.info(f"[FILL] {desc} = '{shown}'")
        self.wait_visible(el, desc)
        el.fill(text)

    def check(self, el: Locator, desc: str = "checkbox"):
        self.log.info(f"[CHECK] {desc}")
        self.wait_visible(el, desc)
        el.check()

    def uncheck(self, el: Locator, desc: str = "checkbox"):
        self.log.info(f"[UNCHECK] {desc}")
        self.wait_visible(el, desc)
        el.uncheck()

    def hover(self, el: Locator, desc: str = "elemento"):
        self.log.info(f"[HOVER] {desc}")
        self.wait_visible(el, desc)
        el.hover()

    def focus(self, el: Locator, desc: str = "elemento"):
        self.log.info(f"[FOCUS] {desc}")
        self.wait_visible(el, desc)
        el.focus()

    def press(self, el: Locator, key: str, desc: str = "elemento"):
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
        self.log.info(
            f"[SELECT_OPTION] {desc} (value={value}, label={label}, index={index})"
        )
        self.wait_visible(el, desc)
        # Playwright permite cualquiera de estos
        kwargs = {}
        if value is not None:
            kwargs["value"] = value
        if label is not None:
            kwargs["label"] = label
        if index is not None:
            kwargs["index"] = index
        el.select_option(**kwargs)

    def set_input_files(self, el: Locator, files, desc: str = "input file"):
        self.log.info(f"[SET_INPUT_FILES] {desc} -> {files}")
        self.wait_visible(el, desc)
        el.set_input_files(files)
