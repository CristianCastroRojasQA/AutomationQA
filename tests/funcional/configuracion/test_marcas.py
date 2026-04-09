import pytest

# Importaciones de dependencias del proyecto
from flows.configuracion.adquirente.marcas_flow import MarcasFlow
from pages.menu.configuracion.adquirente_menu_page import AdquirenteMenuPage
from utils.logger import get_logger
from utils.smoke_navigation_runner import ejecutar_logout_seguro


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
        logger_test.info("Paso 1: Iniciando flujo de autenticación (LOGIN).")
        try:
            auth.login_con_env(caso=nombre_caso_prueba)
            logger_test.info("Login exitoso.")
        except Exception as e:
            logger_test.critical(f"FALLO CRÍTICO: No se pudo realizar el login. Error: {e}", exc_info=True)
            pytest.fail(f"El test no puede continuar sin un login exitoso. Error: {e}")

        logger_test.info("Paso 2: Navegación a 'Marcas y Modelos de Terminales' (ABCUC022).")
        menu_adquirente = AdquirenteMenuPage(page)
        menu_adquirente.navegar_a_adquirente_marcas_y_modelos_terminales(nombre_caso_prueba=nombre_caso_prueba)

        return MarcasFlow(page)

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

            resultado = flow.flujo_alta_registro(valor=marca, logger=logger_test, nombre_caso=nombre_caso_prueba)
            assert resultado, f"Error: La marca '{marca}' no se encontró en la grilla tras guardar."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )

    @pytest.mark.high
    def test_tc02_campo_marca_obligatorio(self, auth, page):
        """TC-02: Verificar bloqueo de inclusión y guardado con campo vacío."""
        nombre_caso_prueba = "TC-MARCAS-02_CampoObligatorio"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            resultado = flow.flujo_validar_campo_obligatorio(logger=logger_test, nombre_caso=nombre_caso_prueba)
            assert resultado, "Error: El sistema no bloqueó correctamente el campo obligatorio."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )

    @pytest.mark.high
    def test_tc03_duplicado_exacto(self, auth, page):
        """TC-03: Verificar que el sistema no permita duplicado exacto."""
        nombre_caso_prueba = "TC-MARCAS-03_DuplicadoExacto"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            nombre_duplicado = "MARCA_DUPLICADA_TEST"
            resultado = flow.flujo_validar_duplicado_exacto(valor=nombre_duplicado, logger=logger_test,
                                                            nombre_caso=nombre_caso_prueba)
            assert resultado, f"Error: El sistema permitió duplicar la marca '{nombre_duplicado}'."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )

    @pytest.mark.high
    def test_tc04_duplicado_logico(self, auth, page):
        """TC-04: Verificar detección de duplicados lógicos (variantes)."""
        nombre_caso_prueba = "TC-MARCAS-04_DuplicadoLogico"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            marca_base = flow.generar_nombre_unico("MARCA_LOGICA")
            resultado = flow.flujo_validar_duplicado_logico(valor=marca_base, logger=logger_test,
                                                            nombre_caso=nombre_caso_prueba)
            assert resultado, "Error en la validación de duplicados lógicos."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )

    @pytest.mark.high
    def test_tc05_eliminar_marca(self, auth, page):
        """TC-05: Verificar que una marca pueda ser eliminada y persista el cambio."""
        nombre_caso_prueba = "TC-MARCAS-05_EliminarMarca"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            marca = flow.generar_nombre_unico("BORRAR-TEST")
            resultado = flow.flujo_eliminar_registro(valor=marca, logger=logger_test, nombre_caso=nombre_caso_prueba)
            assert resultado, f"Error: La marca '{marca}' aún persiste tras la eliminación."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )

    @pytest.mark.high
    def test_tc06_no_success_ante_error(self, auth, page):
        """TC-06: Verificar ausencia de mensaje de éxito ante errores de validación."""
        nombre_caso_prueba = "TC-MARCAS-06_NoSuccessAnteErrores"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            resultado = flow.flujo_validar_no_success_ante_error(logger=logger_test, nombre_caso=nombre_caso_prueba)
            assert resultado, "Error: Se visualizó un mensaje de éxito con datos inválidos."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )

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
            marca = flow.generar_nombre_unico("Marca_Local")
            resultado = flow.flujo_verificar_inclusion_visual_sin_guardar(valor=marca, logger=logger_test,
                                                                          nombre_caso=nombre_caso_prueba)
            assert resultado, "Error: El registro no apareció localmente en el grid."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )

    @pytest.mark.medium
    def test_tc08_eliminar_sin_seleccion(self, auth, page):
        """TC-08: Verificar estado deshabilitado del botón Eliminar sin selección."""
        nombre_caso_prueba = "TC-MARCAS-08_EliminarSinSeleccion"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            # Nota: Usamos la lógica de aserción directa sobre el estado del botón definida en el flow o page
            assert flow.ui.es_boton_eliminar_deshabilitado(), "Error: El botón Eliminar no está deshabilitado."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )

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
            resultado = flow.flujo_validar_longitud_maxima(logger=logger_test, nombre_caso=nombre_caso_prueba)
            assert resultado, "Error: El campo no respetó el límite máximo de caracteres."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )

    @pytest.mark.low
    def test_tc10_persistencia_reload(self, auth, page):
        """TC-10: Asegurar que los datos permanezcan tras un refresco de página."""
        nombre_caso_prueba = "TC-MARCAS-10_PersistenciaReload"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            marca = flow.generar_nombre_unico("RELOAD")
            resultado = flow.flujo_validar_persistencia_reload(valor=marca, logger=logger_test,
                                                               nombre_caso=nombre_caso_prueba)
            assert resultado, "Error Crítico: El dato se perdió tras el reload."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )

    @pytest.mark.low
    def test_tc11_texto_mensaje_success(self, auth, page):
        """TC-11: Verificar que el mensaje Success aparezca tras un guardado válido."""
        nombre_caso_prueba = "TC-MARCAS-11_TextoConfirmacion"
        logger_test = get_logger(nombre_caso_prueba)

        try:
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)
            marca = flow.generar_nombre_unico("MSJ_OK")
            # El flujo de alta ya verifica la alerta de éxito internamente
            resultado = flow.flujo_alta_registro(valor=marca, logger=logger_test, nombre_caso=nombre_caso_prueba)
            assert resultado, "Error: No se visualizó el mensaje de éxito esperado."


        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba,
            )
