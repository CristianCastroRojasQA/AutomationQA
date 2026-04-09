import pytest

from flows.configuracion.adquirente.marcas_flow import MarcasFlow
from flows.configuracion.adquirente.tecnologia_flow import TecnologiaFlow
from pages.menu.configuracion.adquirente_menu_page import AdquirenteMenuPage
from repository.configuracion.adquirente.marcas_repository import MarcasRepository
from repository.configuracion.adquirente.tecnologias_repository import TecnologiaRepository
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_logout_seguro


class TestTecnologiaE2E:
    # ------------------------------------------------------------------
    # Helper para login y navegación
    # ------------------------------------------------------------------
    @staticmethod
    def _login_y_navegar(auth, page, nombre_caso_prueba, logger_test):
        logger_test.info("Paso 1: Iniciando flujo de autenticación (LOGIN).")
        try:
            auth.login_con_env(caso=nombre_caso_prueba)
            logger_test.info("Login exitoso.")
        except Exception as e:
            logger_test.critical(
                f"FALLO CRÍTICO: No se pudo realizar el login. Error: {e}",
                exc_info=True
            )
            pytest.fail(f"El test no puede continuar sin un login exitoso. Error: {e}")

        logger_test.info("Paso 2: Navegación a 'Marcas y Modelos de Terminales' (ABCUC022).")
        menu_adquirente = AdquirenteMenuPage(page)
        menu_adquirente.navegar_a_adquirente_marcas_y_modelos_terminales(
            nombre_caso_prueba=nombre_caso_prueba
        )

        return TecnologiaFlow(page)

    @pytest.mark.e2e
    @pytest.mark.db
    @pytest.mark.high
    @pytest.mark.tecnologia
    def test_tc01_validar_alta_y_baja_tecnologia_ui_vs_db(self, auth, page, db_instance):
        """
        TC-01: Ciclo funcional de Alta y Baja validando contra DB usando el Repositorio.
        """
        nombre_caso_prueba = "TC-TECNOLOGIA-01_Alta_Baja_UI_DB"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flujo = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            repo_tecnologia = TecnologiaRepository(
                db_manager=db_instance,
                nombre_caso_prueba=nombre_caso_prueba
            )
            tecnologia = flujo.generar_nombre_unico("E2E_TECNOLOGIA")

            resultado = flujo.flujo_ciclo_completo_con_db(
                valor=tecnologia,
                logger=logger_test,
                nombre_caso=nombre_caso_prueba,
                repo_db=repo_tecnologia,
                query_sql=repo_tecnologia.SELECT_TECNOLOGIA_BY_NOMBRE

            )
            assert resultado, f"Fallo en la validación E2E para la tecnología: {tecnologia}"
        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )
