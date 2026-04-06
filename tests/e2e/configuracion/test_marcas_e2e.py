import pytest

from flows.marcas_flow import MarcasFlow
from pages.menu.configuracion.adquirente_menu_page import AdquirenteMenuPage
from repository.configuracion.adquirente.marcas_repository import MarcasRepository
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_logout_seguro


class TestMarcasE2E:
    # ------------------------------------------------------------------
    # Helper para login y navegación
    # ------------------------------------------------------------------
    @staticmethod
    def _login_y_navegar(auth, page, nombre_caso_prueba, logger_test):
        # Inicio del proceso de autenticación
        logger_test.info("Paso 1: Iniciando flujo de autenticación (LOGIN).")
        try:
            auth.login_con_env(caso=nombre_caso_prueba)
            logger_test.info("Login exitoso.")
        except Exception as e:
            # Si el login falla, el test se detiene con fail de pytest
            logger_test.critical(
                f"FALLO CRÍTICO: No se pudo realizar el login. Error: {e}",
                exc_info=True
            )
            pytest.fail(f"El test no puede continuar sin un login exitoso. Error: {e}")

        # Navegación a la pantalla específica del módulo
        logger_test.info("Paso 2: Navegación a 'Marcas y Modelos de Terminales' (ABCUC022).")
        menu_adquirente = AdquirenteMenuPage(page)
        menu_adquirente.navegar_a_adquirente_marcas_y_modelos_terminales(
            nombre_caso_prueba=nombre_caso_prueba
        )

        return MarcasFlow(page)

    @pytest.mark.e2e
    @pytest.mark.db
    @pytest.mark.high
    @pytest.mark.marcas
    def test_tc01_validar_alta_y_baja_marca_ui_vs_db(self, auth, page, db_instance):
        """
        TC-01: Ciclo funcional de Alta y Baja validando contra DB.
        """
        nombre_caso_prueba = "TC-MARCAS-01_Alta_Baja_UI_DB"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"--- INICIO DE PRUEBA: {nombre_caso_prueba} ---")

        try:
            # 1. Login y Navegación
            flujo = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Importacion de Repos
            repo = MarcasRepository(
                db_manager=db_instance,
                nombre_caso_prueba=nombre_caso_prueba
            )

            # 3. Generar nombre de marca único
            nombre_test = flujo.marca_unica("E2E_ALTA_BAJA")

            # 3. Ejecutar flujo de validación
            resultado = flujo.flujo_alta_y_baja_con_auditoria_db(
                nombre_marca=nombre_test,
                logger=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
                repo_db=repo
            )

            # 4. Aserción final
            assert resultado
            logger_test.info(f"--- PRUEBA FINALIZADA EXITOSAMENTE: {nombre_caso_prueba} ---")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )
