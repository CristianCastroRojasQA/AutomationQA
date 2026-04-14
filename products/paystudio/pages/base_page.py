from datetime import datetime
from typing import List, Callable, Optional

from playwright.sync_api import Page, Locator

from core.pages.base_page import BasePage as CoreBasePage
from core.config.settings import settings
from core.utils.screenshots import capturar_evidencia


class BasePage(CoreBasePage):
    """
    BasePage específica de PayStudio. Hereda toda la API genérica de Playwright
    del Core y agrega los elementos transversales propios de la aplicación PayStudio.

    Responsabilidad: locators del Navbar/Footer de PayStudio + métodos de
    navegación y manejo de errores propios de esta aplicación.

    Herencia:
        core.pages.base_page.BasePage (API Playwright genérica)
            └── products.paystudio.pages.base_page.BasePage (contexto PayStudio)
                    └── LoginPage, MarcasPage, etc.
    """

    def __init__(self, page: Page, logger_name: str = "PayStudio.BasePage"):
        # Inyectamos los timeouts desde settings de PayStudio al Core
        super().__init__(
            page=page,
            timeout=settings.TIMEOUT,
            animation_wait=settings.ANIMATION_WAIT,
            logger_name=logger_name
        )

        # ── Locators transversales del Navbar de PayStudio ─────────────────
        self.user_welcome  = page.locator("span[id$='UserWelcome']")
        self.user_dropdown = self.user_welcome.locator("xpath=ancestor::a[1]")

    # =========================================================================
    # MENÚ DE PERFIL
    # =========================================================================

    def abrir_menu_perfil(self) -> None:
        """Despliega el menú de usuario del Navbar de PayStudio."""
        self.log.info("Abriendo menú de perfil de usuario")
        self.click(self.user_dropdown, desc="Menú de usuario (Navbar)")

    def obtener_nombre_usuario(self) -> str:
        """Retorna el nombre del usuario logueado según el Navbar."""
        return self.get_text(self.user_welcome, desc="Nombre de usuario en Navbar")

    # =========================================================================
    # NAVEGACIÓN ESTÁNDAR DE PAYSTUDIO (ASP.NET / UpdatePanel)
    # =========================================================================

    def navegar_a_pagina_estandar(
        self,
        pasos_de_navegacion: List[Callable[[], None]],
        segmento_url_esperado: Optional[str],
        locator_titulo_pagina: Locator,
        nombre_caso_prueba: str,
        etiqueta_evidencia: str
    ) -> str:
        """
        Orquestador de navegación para flujos estándar de PayStudio.

        Ejecuta una secuencia de pasos (clicks/hovers), valida el cambio de URL
        y confirma la carga de la página destino con evidencia visual.

        Args:
            pasos_de_navegacion: Lista de callables que ejecutan la navegación.
            segmento_url_esperado: Fragmento de URL para wait_for_url (puede ser None).
            locator_titulo_pagina: Elemento que confirma que la página cargó.
            nombre_caso_prueba: Identificador del test (usado en screenshots).
            etiqueta_evidencia: Sufijo para el nombre del screenshot.

        Returns:
            str: URL final alcanzada.
        """
        for paso in pasos_de_navegacion:
            paso()

        if segmento_url_esperado:
            self.page.wait_for_url(
                f"**/{segmento_url_esperado}*",
                timeout=self._timeout,
                wait_until="networkidle"
            )

        self.log.warning(
            f"Sincronizando navegación hacia '{segmento_url_esperado}'. "
            "Si el título no aparece, verificar latencia del UpdatePanel."
        )

        try:
            locator_titulo_pagina.wait_for(state="visible", timeout=self._timeout_half)
        except Exception as e:
            self.log.error(
                f"PERMISSION / ACCESS ERROR: No se pudo acceder a '{segmento_url_esperado}'. "
                f"Posible problema de permisos o roles. URL actual: {self.page.url}"
            )
            capturar_evidencia(self.page, nombre_caso_prueba, f"ERROR_PERMISOS_{etiqueta_evidencia}")
            raise e

        self.wait_animation()
        capturar_evidencia(self.page, nombre_caso_prueba, f"Pantalla_{etiqueta_evidencia}")
        self.log.info(f"Navegación exitosa a {segmento_url_esperado or 'página destino'}")

        return self.page.url

    # =========================================================================
    # MANEJO DE ERRORES DE APLICACIÓN (ErrorHandlerControl de PayStudio)
    # =========================================================================

    def verificar_y_manejar_error(self, nombre_ruta: str, nombre_caso_prueba: str) -> None:
        """
        Detecta si PayStudio lanzó su ErrorHandlerControl y genera reporte técnico.

        Raises:
            AssertionError: Si se detecta un error de aplicación activo.
        """
        from products.paystudio.pages.common.error_handler_page import ErrorHandlerPage
        error_page = ErrorHandlerPage(self.page)

        if error_page.hay_error():
            self.log.critical(
                f"¡APP ERROR DETECTADO! Pantalla de error activa durante ruta: {nombre_ruta}"
            )

            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            evidencia_dir = settings.EVIDENCIAS_DIR / fecha_hoy / nombre_caso_prueba
            evidencia_dir.mkdir(parents=True, exist_ok=True)

            detalle   = error_page.obtener_detalle()
            timestamp = datetime.now().strftime("%H-%M-%S")

            capturar_evidencia(self.page, nombre_caso_prueba, f"ERROR_{nombre_ruta}")

            txt_path = evidencia_dir / f"DETALLE_TECNICO_{timestamp}.txt"
            txt_path.write_text(f"Ruta: {nombre_ruta}\n\nDetalle:\n{detalle}", encoding="utf-8")

            error_page.aceptar_y_recuperar()

            raise AssertionError(
                f"Fallo de aplicación detectado en ruta '{nombre_ruta}'. "
                f"Detalle técnico guardado en {txt_path.name}"
            )
