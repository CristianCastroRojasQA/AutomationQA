import pytest

# Importaciones de dependencias del proyecto
from flows.configuracion.adquirente.marcas_flow import MarcasFlow
from pages.menu.configuracion.adquirente_menu_page import AdquirenteMenuPage
from repository.configuracion.adquirente.marcas_repository import MarcasRepository
from utils.common_actions import realizar_login_obligatorio, finalizar_sesion_segura
from utils.logger import get_logger


@pytest.mark.funcional
@pytest.mark.configuracion
@pytest.mark.adquirente
@pytest.mark.marcas
class TestMarcasTerminales:
    # ------------------------------------------------------------------
    # Helper para login y navegación
    # ------------------------------------------------------------------
    @staticmethod
    def _login_y_navegar(auth, page, nombre_caso_prueba, logger_test):
        logger_test.info("--- INICIO PRE-CONDICIÓN: Acceso al módulo de Marcas ---")
        realizar_login_obligatorio(auth, nombre_caso_prueba, logger_test)

        logger_test.debug("Navegación a 'Marcas y Modelos de Terminales' (ABCUC022).")
        menu_adquirente = AdquirenteMenuPage(page)
        menu_adquirente.navegar_a_adquirente_marcas_y_modelos_terminales(nombre_caso_prueba=nombre_caso_prueba)

        return MarcasFlow(page)

    @staticmethod
    def _finalizar_test(auth, logger, nombre_caso):
        """Helper estático para cerrar sesión de forma segura al final de cada test."""
        finalizar_sesion_segura(auth, logger, nombre_caso)

    # ============================================================
    # HIGH SEVERITY
    # ============================================================

    @pytest.mark.high
    def test_tc01_alta_marca_y_persistencia(self, auth, page):
        """TC-01: Validar que una marca válida se crea, se guarda y es visible en la grilla."""
        nombre_caso_prueba = "TC-MARCAS-01_Alta_Marca"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            marca = flow.generar_nombre_unico("Marca_Alta")
            logger_test.debug(f"Dato de prueba generado: {marca}")
            flow.flujo_alta_registro(valor=marca, logger=logger_test, nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.high
    def test_tc02_campo_marca_obligatorio(self, auth, page):
        """TC-02: Verificar bloqueo de inclusión y guardado con campo vacío."""
        nombre_caso_prueba = "TC-MARCAS-02_CampoObligatorio"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            flow.flujo_validar_campo_obligatorio(logger=logger_test, nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.high
    def test_tc03_duplicado_exacto(self, auth, page):
        """TC-03: Verificar que el sistema no permita duplicado exacto."""
        nombre_caso_prueba = "TC-MARCAS-03_DuplicadoExacto"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            nombre_duplicado = "MARCA_DUPLICADA_TEST"
            logger_test.debug(f"Dato de prueba generado: {nombre_duplicado}")
            flow.flujo_validar_duplicado_exacto(valor=nombre_duplicado, logger=logger_test,
                                                nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.high
    def test_tc04_duplicado_logico(self, auth, page):
        """TC-04: Verificar detección de duplicados lógicos (variantes)."""
        nombre_caso_prueba = "TC-MARCAS-04_DuplicadoLogico"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            marca_base = flow.generar_nombre_unico("MARCA_LOGICA")
            logger_test.debug(f"Dato de prueba generado: {marca}")
            flow.flujo_validar_duplicado_logico(valor=marca_base, logger=logger_test,
                                                nombre_caso=nombre_caso_prueba)

        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.high
    def test_tc05_eliminar_marca(self, auth, page):
        """TC-05: Verificar que una marca pueda ser eliminada y persista el cambio."""
        nombre_caso_prueba = "TC-MARCAS-05_EliminarMarca"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            marca = flow.generar_nombre_unico("MARCAS-BORRAR-TEST")
            logger_test.debug(f"Dato de prueba generado: {marca}")
            flow.flujo_eliminar_registro(valor=marca, logger=logger_test, nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.high
    def test_tc06_no_persistencia_ante_error(self, auth, page):
        """TC-06: Verificar registro inválido no persiste antes error de success."""
        nombre_caso_prueba = "TC-MARCAS-06_NoSuccessAnteErrores"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            flow.flujo_validar_guardar_con_error_no_persistente(logger=logger_test, nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    # ============================================================
    # MEDIUM - SEVERITY
    # ============================================================

    @pytest.mark.medium
    def test_tc07_incluir_sin_guardar(self, auth, page):
        """TC-07: Verificar que al dar 'Incluir' la marca sea visible localmente."""
        nombre_caso_prueba = "TC-MARCAS-07_IncluirSinGuardar"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            flow.flujo_verificar_inclusion_visual_sin_guardar(logger=logger_test,
                                                              nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.medium
    def test_tc08_eliminar_sin_seleccion(self, auth, page):
        """TC-08: Verificar estado deshabilitado del botón Eliminar sin selección."""
        nombre_caso_prueba = "TC-MARCAS-08_EliminarSinSeleccion"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            flow.flujo_validar_boton_eliminar_sin_seleccion(logger=logger_test,
                                                            nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    # ============================================================
    # LOW - SEVERITY
    # ============================================================

    @pytest.mark.low
    def test_tc09_longitud_maxima(self, auth, page):
        """TC-09: Verificar límite físico de caracteres en el input."""
        nombre_caso_prueba = "TC-MARCAS-09_LongitudMaxima"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            flow.flujo_validar_longitud_maxima(logger=logger_test, nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.low
    def test_tc10_persistencia_reload(self, auth, page):
        """TC-10: Asegurar que los datos permanezcan tras un refresco de página."""
        nombre_caso_prueba = "TC-MARCAS-10_PersistenciaReload"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            marca = flow.generar_nombre_unico("MARCAS-RELOAD")
            logger_test.debug(f"Dato de prueba generado: {marca}")
            flow.flujo_validar_persistencia_reload(valor=marca, logger=logger_test,
                                                   nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.low
    def test_tc11_texto_mensaje_success(self, auth, page):
        """TC-11: Verificar que el mensaje Success aparezca tras un guardado válido."""
        nombre_caso_prueba = "TC-MARCAS-11_TextoConfirmacion"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            marca = flow.generar_nombre_unico("MARCAS-MSJ_OK")
            logger_test.debug(f"Dato de prueba generado: {marca}")
            flow.flujo_validar_texto_mensaje_success(nombre=marca, logger=logger_test,
                                                     nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.low
    def test_tc12_texto_mensaje_warning(self, auth, page):
        """TC-12: Verificar que el mensaje warnign aparezca tras un registro duplicado."""
        nombre_caso_prueba = "TC-MARCAS-12_TextoAdvertencia"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            marca = flow.generar_nombre_unico("MARCAS-MSJ_DUPLICADO")
            logger_test.debug(f"Dato de prueba generado: {marca}")
            flow.flujo_validar_texto_mensaje_warning(nombre=marca, logger=logger_test,
                                                     nombre_caso=nombre_caso_prueba)
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)

    @pytest.mark.low
    def test_tc13_texto_mensaje_error_relacion(self, auth, page, db_instance):
        """TC-13: Verificar que el mensaje error aparezca tras interntar eliminar un registro relacionado."""
        nombre_caso_prueba = "TC-MARCAS-13_TextoError"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            logger_test.debug("Instanciando MarcasRepository para consulta de integridad referencial.")
            repo_marcas = MarcasRepository(
                db_manager=db_instance,
                nombre_caso_prueba=nombre_caso_prueba
            )
            flow.flujo_validar_texto_error_eliminar_con_relacion(
                logger=logger_test,
                nombre_caso=nombre_caso_prueba,
                repo_db=repo_marcas,
                query_sql=repo_marcas.SELECT_MARCA_WITH_RELATION
            )
        finally:
            self._finalizar_test(auth, logger_test, nombre_caso_prueba)
