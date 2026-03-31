# pages/base_page.py
from datetime import datetime
from pathlib import Path
from typing import List, Callable

from playwright.sync_api import Page, Locator, expect

from pages.common.error_handler_page import ErrorHandlerPage
from config.settings import settings
from utils.logger import get_logger
from utils.screenshots import capturar_evidencia


class BasePage:
    """
    BasePage = wrapper de acciones comunes con Playwright usando Locator.
    - NO tiene selectores: los selectores viven en cada Page Object.
    - NO tiene lógica de negocio: solo acciones atómicas (click, fill, etc).
    - SI tiene logs consistentes: para trazabilidad total en la consola.
    """

    URL_TIMEOUT = settings.TIMEOUT
    TITLE_TIMEOUT = settings.TIMEOUT / 2
    ANIMATION_WAIT = settings.ANIMATION_WAIT

    def __init__(self, page: Page, logger_name: str = "BasePage"):
        # Inicializa la página del navegador y el sistema de logs para la clase
        self.page = page
        self.log = get_logger(logger_name)

        # --- COMPONENTES COMUNES (NAVBAR/HEADER) ---
        self.user_welcome = page.locator("span[id$='UserWelcome']")
        self.user_dropdown = self.user_welcome.locator("xpath=ancestor::a[1]")

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

    def abrir_menu_perfil(self):
        """Despliegue del menu usuario"""
        self.click(self.user_dropdown, desc="Abrir menú de usuario")

    def obtener_nombre_usuario(self) -> str:
        """Obtiene el nombre del usuario logueado desde el Navbar."""
        return self.get_text(self.user_welcome, desc="Nombre de usuario en Navbar")

    def navegar_a_pagina_estandar(
            self,
            pasos_de_navegacion: List[Callable[[], None]],
            segmento_url_esperado: str | None,
            locator_titulo_pagina: Locator,
            nombre_caso_prueba: str,
            etiqueta_evidencia: str
    ) -> str:
        """
        Ejecuta una secuencia de pasos para navegar a una página, espera su carga,
        captura una evidencia y retorna la URL actual.

        Args:
            pasos_de_navegacion: Lista de funciones callable (clicks, hovers).
            segmento_url_esperado: Segmento de la URL esperado.
            locator_titulo_pagina: Locator del título de la página destino.
            nombre_caso_prueba: Nombre del caso para logs/evidencia.
            etiqueta_evidencia: Etiqueta para el archivo PNG.
        Returns:
            La URL actual de la página.
        """

        for paso in pasos_de_navegacion:
            paso()
        """Validar URL si se espera"""
        if segmento_url_esperado:
            self.page.wait_for_url(f"**/{segmento_url_esperado}*", timeout=self.URL_TIMEOUT, wait_until="networkidle")

        """Validación obligatoria de visibilidad"""
        locator_titulo_pagina.wait_for(state="visible", timeout=self.TITLE_TIMEOUT)
        self.page.wait_for_timeout(self.ANIMATION_WAIT)

        capturar_evidencia(self.page, nombre_caso_prueba, f"Pantalla_{etiqueta_evidencia}")
        self.log.info(f"Navegación exitosa a {segmento_url_esperado}")
        return self.page.url

    def verificar_y_manejar_error(
            self,
            *,
            nombre_ruta: str,
            nombre_caso_prueba: str
    ):
        """
        Verifica si apareció la página de error y captura evidencias.
        """
        # 1. Corregido: Solo pasamos 'page' si el init de ErrorHandlerPage solo pide page
        error_page = ErrorHandlerPage(self.page)

        if error_page.hay_error():
            root_dir = Path(__file__).resolve().parent.parent
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            evidencia_dir = root_dir / "screenshots" / fecha_hoy / nombre_caso_prueba
            evidencia_dir.mkdir(parents=True, exist_ok=True)

            # 3. Corregido: Si 'guardar_evidencias' no existe en la clase,
            # usamos nuestras utilidades globales aquí directamente.
            detalle = error_page.obtener_detalle()
            timestamp = datetime.now().strftime("%H-%M-%S")

            # Captura PNG
            capturar_evidencia(self.page, nombre_caso_prueba, f"PAGINA_ERROR_{nombre_ruta}")

            # Captura TXT (Detalle técnico)
            txt_path = evidencia_dir / f"{timestamp}_DETALLE_TECNICO.txt"
            txt_path.write_text(f"Ruta: {nombre_ruta}\n\nDetalle:\n{detalle}", encoding="utf-8")

            # 4. Recuperación
            error_page.aceptar_y_recuperar()

            raise AssertionError(
                f"Página de error detectada en navegación: {nombre_ruta}. "
                f"Evidencia guardada en: {evidencia_dir}"
            )
