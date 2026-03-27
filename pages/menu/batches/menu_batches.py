from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import Callable


class MenuBatchesPage(BasePage):
    """
    Clase base para la página del menú principal de Batches.
    Maneja la entrada a la consola y la navegación entre pestañas laterales.
    """

    def __init__(self, page: Page, logger_name: str = "MenuBatches"):
        super().__init__(page, logger_name=logger_name)

        # NIVEL 1: Menú principal de Batches
        self.link_menu_principal_batches = page.locator("#BATCH_KEY")
        self.log.debug(f"Inicializando locators para {self.__class__.__name__}.")
        self.log.debug(f"Locator 'link_menu_principal_batches' inicializado.")

        # NIVEL 2: CONSOLA BATCH (Sub-dropdown)
        self.sub_menu_consola_batches = page.locator("#BatchConsole")
        self.log.debug("Locator 'sub_menu_consola_batches' inicializado.")

        # CONTENEDOR LATERAL: Para evitar errores de "múltiples elementos"
        self.contenedor_grupos = page.locator("#ctl00_ContentPlaceHolder1_UpdatePanel1")
        self.log.debug("Locator 'contenedor_grupos' inicializado.")

        # GRUPOS DE PROCESOS (Usando el patrón de texto dentro del contenedor lateral)
        self.grupo_transaccion_adquirente = self.contenedor_grupos.get_by_role("link", name="Transacción Adquirente")
        self.log.debug("Locator 'grupo_transaccion_adquirente' inicializado.")

        self.grupo_comercial_adquirente = self.contenedor_grupos.get_by_role("link", name="Comercial Adquirente")
        self.log.debug("Locator 'grupo_comercial_adquirente' inicializado.")

        self.grupo_adquirente = self.contenedor_grupos.get_by_role("link", name="Adquirente", exact=True)
        self.log.debug("Locator 'grupo_adquirente' inicializado.")

        self.grupo_comercio_adquirente = self.contenedor_grupos.get_by_role("link", name="Comercio Adquirente")
        self.log.debug("Locator 'grupo_comercio_adquirente' inicializado.")

        self.grupo_comun = self.contenedor_grupos.get_by_role("link", name="Común")
        self.log.debug("Locator 'grupo_comun' inicializado.")

        self.grupo_reportes_adquirente = self.contenedor_grupos.get_by_role("link", name="Reportes Adquirente")
        self.log.debug("Locator 'grupo_reportes_adquirente' inicializado.")

        self.log.info(f"Page Object '{self.__class__.__name__}' inicializado correctamente.")

    # ------------------------------------------------------------------
    # Pasos reutilizables para construir secuencias de navegación
    # ------------------------------------------------------------------

    def abrir_menu_batches(self):
        self.click(self.link_menu_principal_batches, desc="Menú Batches")

    def abrir_consola_batches(self):
        self.click(self.sub_menu_consola_batches, desc="Consola Batches")

    def _obtener_paso_abrir_menu_batches(self) -> Callable[[], None]:
        return lambda: self.abrir_menu_batches()

    def _obtener_paso_abrir_consola_batches(self) -> Callable[[], None]:
        return lambda: self.abrir_consola_batches()

    # ------------------------------------------------------------------
    # Métodos de Navegación a Páginas Específicas
    # ------------------------------------------------------------------

    def navegar_a_consola_batches(self, nombre_caso_prueba: str) -> str:
        """PASO INICIAL: Entra a la Consola de Batches desde el Home."""
        self.log.info(f"Iniciando navegación a 'Consola Batches' para el caso: '{nombre_caso_prueba}'.")

        pasos = [
            self._obtener_paso_abrir_menu_batches(),
            self._obtener_paso_abrir_consola_batches()
        ]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="BatchConsole",
            # Usamos un heading que contenga el texto del título esperado
            locator_titulo_pagina=self.page.get_by_text("Grupos de procesos", exact=True),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Batches_Consola_Principal",
        )

    def navegar_a_grupo_transaccion_adquirente(self, nombre_caso_prueba: str) -> str:
        """Navega al grupo 'Transacción Adquirente'."""
        self.log.info(f"Iniciando navegación a 'Transacción Adquirente' para el caso: '{nombre_caso_prueba}'.")
        pasos = [lambda: self.click(self.grupo_transaccion_adquirente, desc="Grupo Transacción Adquirente")]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="BatchConsole",
            locator_titulo_pagina=self.page.get_by_role("heading").filter(has_text="Transacción Adquirente"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Batches_Transaccion_Adquirente",
        )

    def navegar_a_grupo_comercial_adquirente(self, nombre_caso_prueba: str) -> str:
        """Navega al grupo 'Comercial Adquirente'."""
        self.log.info(f"Iniciando navegación a 'Comercial Adquirente' para el caso: '{nombre_caso_prueba}'.")
        pasos = [lambda: self.click(self.grupo_comercial_adquirente, desc="Grupo Comercial Adquirente")]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="BatchConsole",
            locator_titulo_pagina=self.page.get_by_role("heading").filter(has_text="Comercial Adquirente").first,
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Batches_Comercial_Adquirente",
        )

    def navegar_a_grupo_adquirente(self, nombre_caso_prueba: str) -> str:
        """Navega al grupo 'Adquirente'."""
        self.log.info(f"Iniciando navegación a 'Adquirente' para el caso: '{nombre_caso_prueba}'.")
        pasos = [lambda: self.click(self.grupo_adquirente, desc="Grupo Adquirente")]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="BatchConsole",
            locator_titulo_pagina=self.page.get_by_role("heading").get_by_text("Adquirente", exact=True),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Batches_Adquirente",
        )

    def navegar_a_grupo_comercio_adquirente(self, nombre_caso_prueba: str) -> str:
        """Navega al grupo 'Comercio Adquirente'."""
        self.log.info(f"Iniciando navegación a 'Comercio Adquirente' para el caso: '{nombre_caso_prueba}'.")
        pasos = [lambda: self.click(self.grupo_comercio_adquirente, desc="Grupo Comercio Adquirente")]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="BatchConsole",
            locator_titulo_pagina=self.page.get_by_role("heading").filter(has_text="Comercio Adquirente"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Batches_Comercio_Adquirente",
        )

    def navegar_a_grupo_comun(self, nombre_caso_prueba: str) -> str:
        """Navega al grupo 'Común'."""
        self.log.info(f"Iniciando navegación a 'Común' para el caso: '{nombre_caso_prueba}'.")
        pasos = [lambda: self.click(self.grupo_comun, desc="Grupo Común")]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="BatchConsole",
            locator_titulo_pagina=self.page.get_by_role("heading").filter(has_text="Común"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Batches_Comun",
        )

    def navegar_a_grupo_reportes_adquirente(self, nombre_caso_prueba: str) -> str:
        """Navega al grupo 'Reportes Adquirente'."""
        self.log.info(f"Iniciando navegación a 'Reportes Adquirente' para el caso: '{nombre_caso_prueba}'.")
        pasos = [lambda: self.click(self.grupo_reportes_adquirente, desc="Grupo Reportes Adquirente")]

        return self.navegar_a_pagina_estandar(
            pasos_de_navegacion=pasos,
            segmento_url_esperado="BatchConsole",
            locator_titulo_pagina=self.page.get_by_role("heading").filter(has_text="Reportes Adquirente"),
            nombre_caso_prueba=nombre_caso_prueba,
            etiqueta_evidencia="Batches_Reportes_Adquirente",
        )
