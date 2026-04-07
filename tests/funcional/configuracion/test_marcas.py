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

    # ============================================================
    # HIGH SEVERITY
    # ============================================================

    @pytest.mark.high
    def test_tc01_alta_marca_y_persistencia(self, auth, page):
        """
        TC-01: Validar que una marca válida se crea, se guarda y es visible en la grilla.
        """
        nombre_caso_prueba = "TC-MARCAS-01_Alta_Marca"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación automática
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Generar nombre de marca único
            marca = flow.marca_unica("Marca_Alta")

            # 3. Ejecutar el flujo funcional completo
            resultado = flow.flujo_alta_marca(nombre=marca, logger=logger_test, nombre_caso_prueba=nombre_caso_prueba)

            assert resultado, f"Error: La marca '{marca}' no se encontró en la grilla tras guardar."

            logger_test.info(f"PRUEBA FINALIZADA CON ÉXITO: {nombre_caso_prueba}")

        finally:
            # Cerrar sesión siempre, sin importar el resultado
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.high
    def test_tc02_campo_marca_obligatorio(self, auth, page):
        """
        TC-02: Verificar que el sistema impida la inclusión y el guardado
        cuando el campo 'Marca' está vacío.
        """
        nombre_caso_prueba = "TC-MARCAS-02_CampoObligatorio"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación automática
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Ejecutar el flujo funcional completo
            resultado = flow.flujo_validar_campo_obligatorio(logger=logger_test, nombre_caso_prueba=nombre_caso_prueba)

            # 3. Aserción final
            assert resultado, (
                "Error: El sistema permitió incluir/guardar una marca vacía "
                "o no mostró el mensaje de error correspondiente."
            )

            logger_test.info(f"PRUEBA FINALIZADA CON ÉXITO: {nombre_caso_prueba}")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.high
    def test_tc03_duplicado_exacto(self, auth, page):
        """
        TC-03: Verificar que el sistema no permita la creación de una marca
        con un nombre que ya se encuentra registrado (Duplicado Exacto).
        """

        nombre_caso_prueba = "TC-MARCAS-03_DuplicadoExacto"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            nombre_duplicado = "MARCA_DUPLICADA_TEST"

            resultado = flow.flujo_validar_duplicado_exacto(nombre=nombre_duplicado, logger=logger_test,
                                                            nombre_caso_prueba=nombre_caso_prueba)

            # 4. Aserción final
            assert resultado, (
                f"Error: El sistema permitió duplicar la marca '{nombre_duplicado}' "
                "o no mostró el mensaje de advertencia esperado."
            )

            logger_test.info(f"PRUEBA FINALIZADA CON ÉXITO: {nombre_caso_prueba}")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.high
    def test_tc04_duplicado_logico(self, auth, page):
        """
        TC-04: Verificar que el sistema detecte duplicados lógicos (ignorando
        mayúsculas y espacios adicionales) para mantener la integridad de los datos.
        """
        nombre_caso_prueba = "TC-MARCAS-04_DuplicadoLogico"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Marca base para la prueba
            marca = flow.marca_unica("MARCA_LOGICA")

            # 3. Ejecutar validación de variantes
            resultado = flow.flujo_validar_duplicado_logico(nombre=marca, logger=logger_test,
                                                            nombre_caso_prueba=nombre_caso_prueba)
            # 4. Aserción final
            assert resultado, "Error en la validación de duplicados lógicos."

            logger_test.info(f"PRUEBA FINALIZADA CON ÉXITO: {nombre_caso_prueba}")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.high
    def test_tc05_eliminar_marca(self, auth, page):
        """
        TC-05: Verificar que una marca pueda ser eliminada del grid y que
        dicho cambio se persista correctamente tras guardar.
        """
        nombre_caso_prueba = "TC-MARCAS-05_EliminarMarca"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Generar nombre de marca para la prueba
            marca = flow.marca_unica("BORRAR-TEST")

            # 3. Ejecutar flujo de eliminación
            resultado = flow.flujo_eliminar_marca(nombre=marca, logger=logger_test,
                                                  nombre_caso_prueba=nombre_caso_prueba)
            # 4. Aserción final
            assert resultado, f"Error: La marca '{marca}' aún persiste en el sistema."
            logger_test.info(f"--- PRUEBA FINALIZADA EXITOSAMENTE: {nombre_caso_prueba} ---")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.high
    def test_tc06_no_success_ante_error(self, auth, page):
        """
        TC-06: Verificar que el sistema no despliegue el mensaje de éxito (Success)
        cuando existan errores de validación pendientes en el formulario.
        """
        nombre_caso_prueba = "TC-MARCAS-06_NoSuccessAnteErrores"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación
            flujo = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Ejecutar validación de seguridad de mensajes
            resultado = flujo.flujo_validar_no_success_ante_error(logger_test, nombre_caso_prueba)

            # 3. Aserción final
            assert resultado, "Error de lógica: Se visualizó un mensaje de éxito con datos inválidos."

            logger_test.info(f"--- PRUEBA FINALIZADA EXITOSAMENTE: {nombre_caso_prueba} ---")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    # ============================================================
    #  MEDIUM - SEVERITY
    # ============================================================

    @pytest.mark.medium
    def test_tc07_incluir_sin_guardar(self, auth, page):
        """
        TC-07: Verificar que al dar 'Incluir', la marca se visualice en la tabla
        sin haber presionado 'Guardar' todavía.
        """
        nombre_caso_prueba = "TC-MARCAS-07_IncluirSinGuardar"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación automática
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Generar nombre de marca único
            marca = flow.marca_unica("Marca_Local")

            # 3. Ejecutar el flujo funcional completo
            resultado = flow.flujo_verificar_inclusion_sin_guardar(nombre=marca, logger=logger_test,
                                                                   nombre_caso_prueba=nombre_caso_prueba)
            assert resultado, "Error: La marca no se visualizó en la grilla tras presionar Incluir."

            logger_test.info(f"PRUEBA FINALIZADA CON ÉXITO: {nombre_caso_prueba}")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.medium
    def test_tc08_eliminar_sin_seleccion(self, auth, page):
        """
        TC-08: Verificar que el botón 'Eliminar' permanezca deshabilitado
        mientras no exista una marca seleccionada en la grilla.
        """
        nombre_caso_prueba = "TC-MARCAS-08_EliminarSinSeleccion"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Ejecutar validación de estado de botón
            resultado = flow.flujo_validar_boton_eliminar_sin_seleccion(logger=logger_test,
                                                                        nombre_caso_prueba=nombre_caso_prueba)

            # 3. Aserción final
            assert resultado, "Error: El sistema permite clickear 'Eliminar' sin seleccionar una marca."

            logger_test.info(f"--- PRUEBA FINALIZADA EXITOSAMENTE: {nombre_caso_prueba} ---")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    # ============================================================
    #  LOW - SEVERITY
    # ============================================================

    @pytest.mark.low
    def test_tc09_longitud_maxima(self, auth, page):
        """
        TC-09: Verificar que el campo 'Marca' esté limitado físicamente
        a un máximo de 60 caracteres.
        """
        nombre_caso_prueba = "TC-MARCAS-09_LongitudMaxima"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Ejecutar validación de longitud máxima
            resultado = flow.flujo_validar_longitud_maxima(logger=logger_test, nombre_caso_prueba=nombre_caso_prueba)

            # 3. Aserción final
            assert resultado, (
                f"Error: El campo no respetó el límite de 60 caracteres. "
                f"Se detectó una longitud diferente."
            )

            logger_test.info(f"PRUEBA FINALIZADA CON ÉXITO: {nombre_caso_prueba}")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.low
    def test_tc10_persistencia_reload(self, auth, page):
        """
        TC-10: Asegurar que los datos guardados en el sistema permanezcan
        disponibles tras un refresco de página (Reload).
        """
        nombre_caso_prueba = "TC-MARCAS-10_PersistenciaReload"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Generar nombre de marca único
            marca = flow.marca_unica("RELOAD")

            # 3. Ejecutar flujo de validación post-recarga
            resultado = flow.flujo_validar_persistencia_reload(nombre=marca, logger=logger_test,
                                                               nombre_caso_prueba=nombre_caso_prueba)

            # 4. Aserción final
            assert resultado, f"Error Crítico: La marca '{marca}' no persistió tras el reload."

            logger_test.info(f"--- PRUEBA FINALIZADA EXITOSAMENTE: {nombre_caso_prueba} ---")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )

    @pytest.mark.low
    def test_tc11_texto_mensaje_success(self, auth, page):
        """
        TC-11: Verificar que el texto del mensaje de confirmación tras un
        guardado exitoso sea gramaticalmente correcto y coincida con el diseño.
        """
        nombre_caso_prueba = "TC-MARCAS-11_TextoConfirmacion"
        logger_test = get_logger(nombre_caso_prueba)
        logger_test.info(f"INICIO: Ejecutando {nombre_caso_prueba}")

        try:
            # 1. Login y Navegación
            flow = self._login_y_navegar(auth, page, nombre_caso_prueba, logger_test)

            # 2. Dato único
            marca = flow.marca_unica("MSJ_OK")

            # 3. Ejecutar validación de texto
            resultado = flow.flujo_validar_texto_mensaje_success(nombre=marca, logger=logger_test,
                                                                 nombre_caso_prueba=nombre_caso_prueba)

            # 4. Aserción final
            assert resultado, "Error: El texto del mensaje de éxito no es el correcto."

            logger_test.info(f"--- PRUEBA FINALIZADA EXITOSAMENTE: {nombre_caso_prueba} ---")

        finally:
            ejecutar_logout_seguro(
                flujo_autenticacion=auth,
                logger_test=logger_test,
                nombre_caso_prueba=nombre_caso_prueba
            )
