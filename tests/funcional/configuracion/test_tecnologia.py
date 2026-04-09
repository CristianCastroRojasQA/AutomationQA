import pytest

# Importaciones de dependencias del proyecto
from flows.configuracion.adquirente.tecnologia_flow import TecnologiaFlow
from pages.menu.configuracion.adquirente_menu_page import AdquirenteMenuPage
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_logout_seguro


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
        logger_test.info("Paso 1: Iniciando flujo de autenticación (LOGIN).")
        try:
            auth.login_con_env(caso=nombre_caso_prueba)
            logger_test.info("Login exitoso.")
        except Exception as e:
            logger_test.critical(
                f"FALLO CRÍTICO: No se pudo realizar el login. Error: {e}",
                exc_info=True
            )
            pytest.fail(
                f"El test no puede continuar sin un login exitoso. Error: {e}"
            )

        logger_test.info("Paso 2: Navegación a 'Tecnologías de Terminales'.")
        menu_adquirente = AdquirenteMenuPage(page)
        menu_adquirente.navegar_a_adquirente_marcas_y_modelos_terminales(
            nombre_caso_prueba=nombre_caso_prueba
        )

        return TecnologiaFlow(page)

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

            resultado = flow.flujo_alta_registro(
                valor=tecnologia,
                logger=logger_test,
                nombre_caso=nombre_caso_prueba
            )

            assert resultado

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.high
    def test_tc02_campo_tecnologia_obligatorio(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-02_CampoObligatorio"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            resultado = flow.flujo_validar_campo_obligatorio(
                logger=logger_test,
                nombre_caso=nombre_caso_prueba
            )

            assert resultado

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.high
    def test_tc03_duplicado_exacto(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-03_DuplicadoExacto"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            nombre_duplicado = "TEC_DUPLICADA_TEST"

            resultado = flow.flujo_validar_duplicado_exacto(
                valor=nombre_duplicado,
                logger=logger_test,
                nombre_caso=nombre_caso_prueba
            )

            assert resultado

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.high
    def test_tc04_duplicado_logico(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-04_DuplicadoLogico"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia_base = flow.generar_nombre_unico("TEC_LOGICA")

            resultado = flow.flujo_validar_duplicado_logico(
                valor=tecnologia_base,
                logger=logger_test,
                nombre_caso=nombre_caso_prueba
            )

            assert resultado

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.high
    def test_tc05_eliminar_tecnologia(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-05_EliminarTecnologia"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia = flow.generar_nombre_unico("BORRAR_TEC")

            resultado = flow.flujo_eliminar_registro(
                valor=tecnologia,
                logger=logger_test,
                nombre_caso=nombre_caso_prueba
            )

            assert resultado

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.high
    def test_tc06_no_success_ante_error(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-06_NoSuccessAnteErrores"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            resultado = flow.flujo_validar_no_success_ante_error(
                logger=logger_test,
                nombre_caso=nombre_caso_prueba
            )

            assert resultado
        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    # ============================================================
    # MEDIUM SEVERITY
    # ============================================================

    @pytest.mark.medium
    def test_tc07_incluir_sin_guardar(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-07_IncluirSinGuardar"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia = flow.generar_nombre_unico("TEC_LOCAL")

            resultado = flow.flujo_verificar_inclusion_visual_sin_guardar(
                valor=tecnologia,
                logger=logger_test,
                nombre_caso=nombre_caso_prueba
            )

            assert resultado
        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.medium
    def test_tc08_eliminar_sin_seleccion(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-08_EliminarSinSeleccion"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            assert flow.ui.es_boton_eliminar_deshabilitado()
        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    # ============================================================
    # LOW SEVERITY
    # ============================================================

    @pytest.mark.low
    def test_tc09_longitud_maxima(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-09_LongitudMaxima"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            resultado = flow.flujo_validar_longitud_maxima(
                logger=logger_test,
                nombre_caso=nombre_caso_prueba
            )

            assert resultado
        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.low
    def test_tc10_persistencia_reload(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-10_PersistenciaReload"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia = flow.generar_nombre_unico("TEC_RELOAD")

            resultado = flow.flujo_validar_persistencia_reload(
                valor=tecnologia,
                logger=logger_test,
                nombre_caso=nombre_caso_prueba
            )

            assert resultado
        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.low
    def test_tc11_texto_mensaje_success(self, auth, page):
        nombre_caso_prueba = "TC-TECNOLOGIA-11_TextoConfirmacion"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            tecnologia = flow.generar_nombre_unico("TEC_MSJ")

            resultado = flow.flujo_alta_registro(
                valor=tecnologia,
                logger=logger_test,
                nombre_caso=nombre_caso_prueba
            )

            assert resultado
        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )
