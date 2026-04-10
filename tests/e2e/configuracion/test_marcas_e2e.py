import pytest

from flows.configuracion.adquirente.marcas_flow import MarcasFlow
from pages.menu.configuracion.adquirente_menu_page import AdquirenteMenuPage
from repository.configuracion.adquirente.marcas_repository import MarcasRepository
from utils.common_actions import realizar_login_obligatorio, finalizar_sesion_segura
from utils.logger import get_logger


class TestMarcasE2E:
    # ------------------------------------------------------------------
    # Helper para login y navegación
    # ------------------------------------------------------------------
    @staticmethod
    def _login_y_navegar(auth, page, nombre_caso_prueba, logger_test):
        logger_test.info("Paso 1: Iniciando flujo de autenticación (LOGIN).")
        realizar_login_obligatorio(auth, nombre_caso_prueba, logger_test)

        logger_test.info("Paso 2: Navegación a 'Marcas y Modelos de Terminales' (ABCUC022).")
        menu_adquirente = AdquirenteMenuPage(page)
        menu_adquirente.navegar_a_adquirente_marcas_y_modelos_terminales(
            nombre_caso_prueba=nombre_caso_prueba
        )

        return MarcasFlow(page)

    @staticmethod
    def _finalizar_test(auth, logger, nombre_caso):
        """Helper estático para cerrar sesión de forma segura al final de cada test."""
        finalizar_sesion_segura(auth, logger, nombre_caso)

    @pytest.mark.e2e
    @pytest.mark.db
    @pytest.mark.high
    @pytest.mark.marcas
    def test_tc01_validar_alta_y_baja_marca_ui_vs_db(self, auth, page, db_instance):
        """
        TC-01: Ciclo funcional de Alta y Baja validando contra DB usando el Repositorio.
        """
        nombre_caso_prueba = "TC-MARCAS-01_Alta_Baja_UI_DB"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flujo = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            repo_marcas = MarcasRepository(
                db_manager=db_instance,
                nombre_caso_prueba=nombre_caso_prueba
            )
            marca = flujo.generar_nombre_unico("E2E_MARCA")

            flujo.flujo_ciclo_completo_con_db(
                valor=marca,
                logger=logger_test,
                nombre_caso=nombre_caso_prueba,
                repo_db=repo_marcas,
                query_sql=repo_marcas.SELECT_MARCA_BY_NOMBRE
            )
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)
