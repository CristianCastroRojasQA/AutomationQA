import pytest

# Importaciones de dependencias del proyecto
from flows.configuracion.adquirente.tecnologias_flow import TecnologiasFlow
from pages.menu.configuracion.adquirente_menu_page import AdquirenteMenuPage
from repository.configuracion.adquirente.tecnologias_repository import TecnologiasRepository
from utils.common_actions import realizar_login_obligatorio, finalizar_sesion_segura
from utils.logger import get_logger


@pytest.mark.funcional
@pytest.mark.configuracion
@pytest.mark.adquirente
@pytest.mark.tecnologia
class TestTecnologiaTerminales:
    # ------------------------------------------------------------------
    # Helper para login y navegación
    # ------------------------------------------------------------------
    @staticmethod
    def _login_y_navegar(auth, page, nombre_caso_prueba, logger_test):
        logger_test.info("--- INICIO PRE-CONDICIÓN: Acceso al módulo de Tecnología ---")
        realizar_login_obligatorio(auth, nombre_caso_prueba, logger_test)

        logger_test.debug("Navegación a 'Marcas y Modelos de Terminales' (ABCUC022).")
        menu_adquirente = AdquirenteMenuPage(page)
        menu_adquirente.navegar_a_adquirente_marcas_y_modelos_terminales(
            nombre_caso_prueba=nombre_caso_prueba
        )

        return TecnologiasFlow(page)

    @staticmethod
    def _finalizar_test(auth, logger, nombre_caso):
        """Helper estático para cerrar sesión de forma segura al final de cada test."""
        finalizar_sesion_segura(auth, logger, nombre_caso)

    # ============================================================
    # HIGH SEVERITY
    # ============================================================

    @pytest.mark.high
    def test_tc01_alta_tecnologia_y_persistencia(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-01_Alta_Tecnologia"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia = flow.generar_nombre_unico("TEC_ALTA")
            logger_test.debug(f"Dato de prueba generado: {tecnologia}")
            flow.flujo_alta_registro(valor=tecnologia, logger=logger_test, nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.high
    def test_tc02_campo_tecnologia_obligatorio(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-02_CampoObligatorio"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            flow.flujo_validar_campo_obligatorio(logger=logger_test, nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.high
    def test_tc03_duplicado_exacto(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-03_DuplicadoExacto"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            nombre_duplicado = "TECNOLOGIA_DUPLICADA_TEST"
            logger_test.debug(f"Dato de prueba generado: {nombre_duplicado}")
            flow.flujo_validar_duplicado_exacto(valor=nombre_duplicado, logger=logger_test,
                                                nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.high
    def test_tc04_duplicado_logico(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-04_DuplicadoLogico"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia = flow.generar_nombre_unico("TECNOLOGIA_LOGICA")
            logger_test.debug(f"Dato de prueba generado: {tecnologia}")
            flow.flujo_validar_duplicado_logico(valor=tecnologia, logger=logger_test,
                                                nombre_caso=nombre_caso_prueba)

        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.high
    def test_tc05_eliminar_tecnologia(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-05_EliminarTecnologia"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia = flow.generar_nombre_unico("TECNOLOGIA-BORRAR-TEST")
            logger_test.debug(f"Dato de prueba generado: {tecnologia}")
            flow.flujo_eliminar_registro(valor=tecnologia, logger=logger_test, nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.high
    def test_tc06_no_success_ante_error(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-06_NoSuccessAnteErrores"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            flow.flujo_validar_guardar_con_error_no_persistente(logger=logger_test, nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    # ============================================================
    # MEDIUM SEVERITY
    # ============================================================

    @pytest.mark.medium
    def test_tc07_incluir_sin_guardar(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-07_IncluirSinGuardar"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            flow.flujo_verificar_inclusion_visual_sin_guardar(logger=logger_test,
                                                              nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.medium
    def test_tc08_eliminar_sin_seleccion(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-08_EliminarSinSeleccion"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            flow.flujo_validar_boton_eliminar_sin_seleccion(logger=logger_test,
                                                            nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    # ============================================================
    # LOW SEVERITY
    # ============================================================

    @pytest.mark.low
    def test_tc09_longitud_maxima(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-09_LongitudMaxima"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            flow.flujo_validar_longitud_maxima(logger=logger_test, nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.low
    def test_tc10_persistencia_reload(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-10_PersistenciaReload"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia = flow.generar_nombre_unico("TECNOLOGIA-RELOAD")
            logger_test.debug(f"Dato de prueba generado: {tecnologia}")
            flow.flujo_validar_persistencia_reload(valor=tecnologia, logger=logger_test,
                                                   nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.low
    def test_tc11_texto_mensaje_success(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-11_TextoConfirmacion"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia = flow.generar_nombre_unico("TEC-MSJ_OK")
            logger_test.debug(f"Dato de prueba generado: {tecnologia}")
            flow.flujo_validar_texto_mensaje_success(nombre=tecnologia, logger=logger_test,
                                                     nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.low
    def test_tc12_texto_mensaje_warning(self, auth, page):
        """TC-12: Verificar que el mensaje warnign aparezca tras un registro duplicado."""
        nombre_caso_prueba = "TC-TECNOLOGIA-12_TextoAdvertencia"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia = flow.generar_nombre_unico("TECNO-MSJ_DUPLICADO")
            logger_test.debug(f"Dato de prueba generado: {tecnologia}")
            flow.flujo_validar_texto_mensaje_warning(nombre=tecnologia, logger=logger_test,
                                                     nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.low
    def test_tc13_texto_mensaje_error_relacion(self, auth, page, db_instance):
        """TC-13: Verificar que el mensaje error aparezca tras interntar eliminar un registro relacionado."""
        nombre_caso_prueba = "TC-TECNOLOGIA-13_TextoError"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            logger_test.debug("Instanciando TecnologiasRepository para consulta de integridad referencial.")
            repo_tecnologia = TecnologiasRepository(
                db_manager=db_instance,
                nombre_caso_prueba=nombre_caso_prueba
            )
            flow.flujo_validar_texto_error_eliminar_con_relacion(
                logger=logger_test,
                nombre_caso=nombre_caso_prueba,
                repo_db=repo_tecnologia,
                query_sql=repo_tecnologia.SELECT_TECNOLOGIA_WITH_RELATION
            )
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)
