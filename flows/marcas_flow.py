import time
from playwright.sync_api import expect

from pages.configuracion.adquirente.marcas_page import MarcasPage
from utils.screenshots import capturar_evidencia
from utils.sql_evidence import capturar_evidencia_sql


class MarcasFlow:
    """
    Clase de flujo funcional para la pantalla de Marcas (ABCUC022).
    Coordina las acciones del Page Object para ejecutar los casos de prueba del 01 al 12.
    """

    def __init__(self, page):
        self.page = page
        self.ui = MarcasPage(page)

    # -------------------------
    # Utilidad: Generación de datos
    # -------------------------
    @staticmethod
    def marca_unica(prefijo="Marca_QA") -> str:
        """Genera un nombre único con timestamp para evitar errores de duplicidad en base de datos."""
        return f"{prefijo}_{int(time.time())}"

    # ============================================================
    # HIGH SEVERITY
    # ============================================================

    def flujo_alta_marca(self, nombre: str, logger, nombre_caso_prueba: str = None):
        """
        Flujo de Negocio: Crea una marca, guarda cambios y verifica que aparezca
        en la grilla navegando por la paginación si es necesario.
        """

        nombre_caso = nombre_caso_prueba

        # PASO 1: Ingresar el nombre de la marca
        logger.info(f"Escribiendo nombre de marca: {nombre}")
        self.ui.escribir_marca(nombre)
        capturar_evidencia(self.page, nombre_caso, "01_Digitacion_Marca")
        logger.info("Evidencia capturada: Marca digitada correctamente.")

        # PASO 2: Incluir en la tabla local
        logger.info("Haciendo clic en 'Incluir'")
        self.ui.click_incluir()

        # PASO 3: Guardar en el servidor
        logger.info("Presionando 'Guardar' para persistencia en base de datos")
        self.ui.click_guardar()

        # PASO 4: Esperar confirmación del sistema
        self.ui.esperar_success()
        logger.info("Mensaje de éxito recibido correctamente")

        # PASO 5: Verificación (Paginación)
        logger.info(f"Buscando '{nombre}' en la grilla de resultados")
        encontrado = self.ui.buscar_marca_en_paginacion(nombre)

        # Registro de evidencia final
        resultado = "Exitosa" if encontrado else "Fallida"
        capturar_evidencia(self.page, nombre_caso, f"03_Busqueda_en_Grilla_{resultado}")
        logger.info("Evidencia capturada: Marca creada correctamente.")
        return encontrado

    def flujo_validar_campo_obligatorio(self, logger, nombre_caso_prueba: str = None):
        """
        Flujo Funcional: Intenta incluir una marca vacía y verifica que el sistema
        muestre el error y no permita agregar la fila ni guardar.
        """

        nombre_caso = nombre_caso_prueba

        # PASO 1: Guardamos el estado inicial de la grilla
        cantidad_inicial = self.ui.cantidad_marcas()
        logger.info(f"Cantidad inicial de filas en la grilla: {cantidad_inicial}")

        # PASO 2: Intentar incluir campo vacío
        logger.info("Intentando incluir una marca con el campo vacío")
        self.ui.escribir_marca("")  # Dejar vacío
        self.ui.click_incluir()

        # PASO 3: Verificar indicadores de error (UI)
        # Validamos si el input tiene la clase de error o si el mensaje es visible
        error_visible = self.ui.input_es_invalido() or self.ui.msg_error_campo().is_visible()
        logger.info(f"¿Se muestra el error de validación?: {error_visible}")
        capturar_evidencia(self.page, nombre_caso, "01_Validacion_Campo_Vacio")

        # PASO 4: Verificar que la grilla NO creció
        cantidad_final = self.ui.cantidad_marcas()
        logger.info(f"Cantidad final de filas: {cantidad_final}")
        es_valido_bloqueo_grilla = (cantidad_final == cantidad_inicial)

        logger.info("Paso 4: Intentando 'Guardar' para verificar bloqueo global")
        self.ui.click_guardar()
        permite_guardar = self.ui.success_visible()
        self.page.evaluate("window.scrollTo(0, 0)")
        capturar_evidencia(self.page, nombre_caso, "02_Bloqueo_Guardar_Global")

        # Retornamos el resultado de todas las validaciones
        return error_visible and es_valido_bloqueo_grilla and not permite_guardar

    def flujo_validar_duplicado_exacto(self, nombre: str, logger, nombre_caso_prueba: str = None):
        """
        Flujo Funcional: Intenta dar de alta una marca con un nombre que ya existe
        y verifica que el sistema muestre una advertencia y bloquee el guardado.
        En caso que exista el busca la marca y valida la duplicidad.
        """

        nombre_caso = nombre_caso_prueba

        logger.info(f"Pre-condición: Buscando marca '{nombre}' en la grilla (paginación).")
        existe = self.ui.buscar_marca_en_paginacion(nombre)

        if not existe:
            logger.info(f"Pre-condición: No existe '{nombre}'. Creando marca base.")
            # Mantén tu firma/uso como lo manejas hoy (solo recomiendo keyword args por seguridad)
            self.flujo_alta_marca(nombre=nombre, logger=logger, nombre_caso_prueba=nombre_caso)
            logger.info(f"Pre-condición: Marca creada. Confirmando presencia en grilla (paginación).")
            self.ui.buscar_marca_en_paginacion(nombre)
        else:
            logger.info(f"Pre-condición: La marca '{nombre}' ya existe. Continuando a validación de duplicidad.")

        # Contamos cuántas veces aparece antes de intentar el duplicado
        ocurrencias_antes = self.ui.grid_cells().filter(has_text=nombre).count()
        logger.info(f"Ocurrencias iniciales de '{nombre}': {ocurrencias_antes}")

        # PASO 1: Intentar duplicar la marca
        logger.info(f"Paso 1: Intentando incluir marca duplicada: {nombre}")
        self.ui.escribir_marca(nombre)
        self.ui.click_incluir()

        # PASO 2: Verificar mensaje de Advertencia (Warning)
        logger.info("Paso 3: Esperando mensaje de advertencia del sistema")
        self.ui.esperar_warning_duplicado()

        # Validamos que NO aparezca el mensaje de éxito
        exito_visible = self.ui.success_visible()
        capturar_evidencia(self.page, nombre_caso, "01_Advertencia_Duplicado_Visible")

        # PASO 3: Verificar que la grilla no aumentó registros con ese nombre
        ocurrencias_despues = self.ui.grid_cells().filter(has_text=nombre).count()
        logger.info(f"Ocurrencias finales de '{nombre}': {ocurrencias_despues}")

        # El test es exitoso si hubo warning, no hubo éxito y la cantidad de filas es igual
        es_valido = not exito_visible and (ocurrencias_antes == ocurrencias_despues)

        return es_valido

    def flujo_validar_duplicado_logico(self, nombre: str, logger, nombre_caso_prueba: str = None):
        """
        Flujo Funcional: Intenta ingresar variantes con espacios y mayúsculas
        de una marca existente para verificar que el sistema las bloquee.
        """

        nombre_caso = nombre_caso_prueba

        # Pre-condición: Asegurar que la marca base existe (buscando en el grid)
        if not self.ui.buscar_marca_en_paginacion(nombre):
            logger.info(f"Pre-condición: Creando marca base '{nombre}'")
            self.flujo_alta_marca(nombre, logger, nombre_caso)
            self.page.reload()

        # Definimos las variantes "tramposas"
        variantes = [
            nombre.lower(),  # En minúsculas
            f" {nombre} ",  # Con espacios a los lados
            nombre.upper() if nombre != nombre.upper() else f"{nombre}  "  # Mayúsculas o doble espacio
        ]

        for i, v in enumerate(variantes):
            logger.info(f"Variante {i + 1}: Intentando con '{v}'")

            # PASO 1: Intentar incluir la variante
            self.ui.escribir_marca(v)
            self.ui.click_incluir()

            # PASO 2: Esperar el Warning de duplicado
            logger.info(f"Esperando advertencia para la variante: '{v}'")
            self.ui.esperar_warning_duplicado()

            # Capturamos evidencia de cada bloqueo
            capturar_evidencia(self.page, nombre_caso, f"0{i + 1}_Bloqueo_Variante_{i + 1}")

            # PASO 3: Verificar que no se haya guardado (No debe haber Success)
            assert not self.ui.success_visible(), f"Error: Se permitió guardar la variante '{v}'"

        # Verificación final: La marca original debe seguir siendo la única
        # (Si buscar_marca_en_paginacion contara, debería devolver 1)
        logger.info("Verificando que no se crearon registros duplicados en el grid")
        return self.ui.buscar_marca_en_paginacion(nombre)

    def flujo_eliminar_marca(self, nombre: str, logger, nombre_caso_prueba: str = None):
        """
        Flujo Funcional: Localiza una marca (incluso en otras páginas),
        la elimina de la grilla y confirma la persistencia con el botón Guardar.
        """

        nombre_caso = nombre_caso_prueba

        # PRE-CONDICIÓN: Asegurar que la marca existe para poder eliminarla
        logger.info(f"Buscando marca '{nombre}' para eliminación...")
        existe = self.ui.buscar_marca_en_paginacion(nombre)

        if not existe:
            logger.info(f"La marca '{nombre}' no existe. Creándola para la prueba...")
            self.flujo_alta_marca(nombre, logger, nombre_caso)
            # Volvemos a buscarla para asegurar que estamos en la página correcta
            self.ui.buscar_marca_en_paginacion(nombre)

        # PASO 1: Seleccionar la marca en el grid
        logger.info(f"Paso 1: Seleccionando la marca '{nombre}' en el grid")
        self.ui.seleccionar_marca_en_grid(nombre)
        capturar_evidencia(self.page, nombre_caso, "01_Marca_Seleccionada")

        # PASO 2: Verificar que el botón Eliminar se habilite y clickearlo
        assert not self.ui.eliminar_deshabilitado(), "Error: El botón Eliminar no se activó al seleccionar."
        logger.info("Paso 2: Haciendo clic en 'Eliminar'")
        self.ui.click_eliminar()

        # PASO 3: Validación visual inmediata (Debe desaparecer de la grilla local)
        logger.info("Paso 3: Verificando remoción visual inmediata")
        expect(self.ui.grid_cells().filter(has_text=nombre)).to_have_count(0)
        capturar_evidencia(self.page, nombre_caso, "02_Remocion_Visual_Grid")

        # PASO 4: Persistencia final
        logger.info("Paso 4: Presionando 'Guardar' para confirmar eliminación en backend")
        self.ui.click_guardar()
        self.ui.esperar_success()

        # PASO 5: Verificación final (No debe existir en ninguna página)
        logger.info("Paso 5: Verificando que la marca ya no existe en el sistema")
        # Intentamos buscarla de nuevo; debería retornar False
        todavia_existe = self.ui.buscar_marca_en_paginacion(nombre)

        capturar_evidencia(self.page, nombre_caso, "03_Confirmacion_Eliminacion_Final")

        return not todavia_existe

    def flujo_validar_no_success_ante_error(self, logger, nombre_caso_prueba: str = None):
        """
        Flujo de Seguridad: Provoca un error de validación y verifica que el sistema
        NO muestre el mensaje de éxito al intentar guardar.
        """

        nombre_caso = nombre_caso_prueba

        # PASO 1: Provocar el error (dejar campo vacío)
        logger.info("Paso 1: Intentando incluir una marca vacía para provocar error")
        self.ui.escribir_marca("")
        self.ui.click_incluir()

        # PASO 2: Intentar guardar a pesar del error
        logger.info("Paso 2: Intentando 'Guardar' con errores activos en el formulario")
        self.ui.click_guardar()

        # PASO 3: Verificación de seguridad
        # El sistema NO debe mostrar el cartel verde de éxito
        exito_visible = self.ui.success_visible()

        logger.info(f"¿Se mostró el mensaje de éxito de forma errónea?: {exito_visible}")
        capturar_evidencia(self.page, nombre_caso, "01_Verificacion_Ausencia_Success")

        if not exito_visible:
            logger.info("Éxito: El sistema bloqueó correctamente el mensaje de confirmación.")
        else:
            logger.error("Fallo Crítico: El sistema mostró 'Éxito' a pesar de tener campos inválidos.")

        return not exito_visible

    # ============================================================
    #  MEDIUM - SEVERITY
    # ============================================================

    def flujo_verificar_inclusion_sin_guardar(self, nombre: str, logger, nombre_caso_prueba: str = None):
        """
        Flujo Funcional: Valida que la marca aparezca en la grilla inmediatamente
        después de presionar 'Incluir', antes de confirmar el guardado global.
        """

        nombre_caso = nombre_caso_prueba

        # PASO 1: Ingresar el nombre de la marca
        logger.info(f"Escribiendo nombre de marca: {nombre}")
        self.ui.escribir_marca(nombre)
        capturar_evidencia(self.page, nombre_caso, "01_Marca_Digitada")
        logger.info("Evidencia capturada: Marca digitada correctamente.")

        # PASO 2: Incluir en la tabla local
        logger.info("Haciendo clic en 'Incluir'")
        self.ui.click_incluir()

        # PASO 3: Verificación visual en el grid
        logger.info(f"Verificando presencia visual de '{nombre}' en la grilla")
        # Usamos expect para asegurar que sea visible antes de la foto
        expect(self.ui.grid_cells().filter(has_text=nombre).first).to_be_visible()
        capturar_evidencia(self.page, nombre_caso, "02_Visualizacion_Inmediata")
        logger.info("Evidencia capturada: Marca creada correctamente.")

        # PASO 4: Cancelamos proceso
        logger.info("Cancelando el proceso para limpiar el formulario")
        self.ui.click_cancelar()

        return True

    def flujo_validar_boton_eliminar_sin_seleccion(self, logger, nombre_caso_prueba: str = None):
        """
        Flujo Funcional: Verifica que al ingresar a la pantalla, sin haber
        tocado nada, el botón 'Eliminar' se encuentre deshabilitado.
        """

        nombre_caso = nombre_caso_prueba

        # PASO 1: Verificar estado inicial del botón
        logger.info("Paso 1: Verificando que el botón 'Eliminar' esté deshabilitado por defecto")

        esta_deshabilitado = self.ui.eliminar_deshabilitado()

        # Capturamos evidencia del estado del botón en la botonera
        capturar_evidencia(self.page, nombre_caso, "01_Boton_Eliminar_Deshabilitado")

        if esta_deshabilitado:
            logger.info("Éxito: El botón se encuentra correctamente bloqueado sin selección.")
        else:
            logger.error("Fallo: El botón 'Eliminar' está habilitado sin haber seleccionado una fila.")

        return esta_deshabilitado

    # ============================================================
    #  LOW - SEVERITY
    # ============================================================

    def flujo_validar_longitud_maxima(self, logger, nombre_caso_prueba: str = None):
        """
        Flujo Funcional: Intenta ingresar un texto de 65 caracteres y verifica
        que el campo lo trunque automáticamente a 60.
        """

        nombre_caso = nombre_caso_prueba

        # Preparamos una cadena de 65 caracteres
        texto_largo = "A" * 65
        logger.info(f"Paso 1: Intentando ingresar texto de {len(texto_largo)} caracteres")

        # PASO 1: Escribir el texto largo
        self.ui.escribir_marca(texto_largo)

        # PASO 2: Obtener lo que quedó realmente en el input
        valor_en_pantalla = self.ui.valor_input()
        longitud_real = len(valor_en_pantalla)

        logger.info(f"Longitud capturada en el campo: {longitud_real}")
        capturar_evidencia(self.page, nombre_caso, f"01_Verificacion_Longitud_{longitud_real}")

        # PASO 3: Validación lógica
        # El atributo 'maxlength' del HTML debería impedir que pase de 60
        es_valido = (longitud_real == 60)

        if es_valido:
            logger.info("Éxito: El campo truncó el texto correctamente a 60 caracteres.")
        else:
            logger.error(f"Fallo: El campo permitió {longitud_real} caracteres.")

        return es_valido

    def flujo_validar_persistencia_reload(self, nombre: str, logger, nombre_caso_prueba: str = None):
        """
        Flujo Funcional: Crea una marca, guarda y fuerza un refresco de la página
        para asegurar que el dato se recupera correctamente desde el servidor.
        """

        nombre_caso = nombre_caso_prueba

        # PASO 1: Alta y Guardado (Reutilizamos el flujo de éxito)
        logger.info(f"Paso 1: Creando y guardando la marca '{nombre}'")
        self.flujo_alta_marca(nombre, logger, nombre_caso)

        # PASO 2: Simular recarga de página (F5)
        logger.info("Paso 2: Recargando la página (Simulando nueva sesión/refresco)")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        capturar_evidencia(self.page, nombre_caso, "01_Pagina_Recargada")

        # PASO 3: Verificación de persistencia real
        logger.info(f"Paso 3: Verificando si '{nombre}' sigue existiendo en el servidor...")
        # Debemos buscar en la paginación porque tras el F5 volvemos a la página 1
        existe = self.ui.buscar_marca_en_paginacion(nombre)

        capturar_evidencia(self.page, nombre_caso, "02_Confirmacion_Persistencia_Post_Recarga")

        if existe:
            logger.info("Éxito: El dato persiste correctamente tras la recarga.")
        else:
            logger.error("Fallo: El dato desapareció tras recargar la página.")

        return existe

    def flujo_validar_texto_mensaje_success(self, nombre: str, logger, nombre_caso_prueba: str = None):
        """
        Flujo Funcional: Crea una marca y valida que el texto del mensaje de éxito
        sea exactamente el definido por los requerimientos del sistema.
        """

        nombre_caso = nombre_caso_prueba

        # Definimos el mensaje esperado según el requerimiento (ajustar según tu app)
        mensaje_esperado = "Marcas y Modelos actualizados correctamente"

        # PASO 1: Alta y Guardado
        logger.info(f"Paso 1: Creando marca '{nombre}' para disparar el mensaje")
        self.ui.escribir_marca(nombre)
        self.ui.click_incluir()
        self.ui.click_guardar()

        # PASO 2: Capturar el texto del mensaje
        logger.info("Paso 2: Esperando y capturando el texto de la alerta de éxito")
        self.ui.esperar_success()

        texto_real = self.ui.SUCCESS_TEXT
        logger.info(f"Texto capturado: '{texto_real}'")

        capturar_evidencia(self.page, nombre_caso, "01_Validacion_Texto_Success")

        # PASO 3: Comparación técnica
        coincide = (texto_real.strip() == mensaje_esperado)

        if coincide:
            logger.info("Éxito: El texto del mensaje coincide con el requerimiento.")
        else:
            logger.error(f"Fallo: Se esperaba '{mensaje_esperado}' pero se leyó '{texto_real}'")

        return coincide

    # ============================================================
    #  E2E - HIGH SEVERITY
    # ============================================================

    def flujo_alta_y_baja_con_auditoria_db(
            self,
            nombre_marca: str,
            logger,
            nombre_caso_prueba: str,
            repo_db
    ):
        """
        Flujo Funcional: Alta de marca y eliminación posterior.
        Valida la existencia y ausencia en DB usando el patrón estándar.
        """
        nombre_caso = nombre_caso_prueba

        # ==========================================================
        # 1. ALTA: Creación de marca y validación en DB
        # ==========================================================
        logger.info(f"Paso 1: Realizando alta de la marca '{nombre_marca}'")

        self.ui.escribir_marca(nombre_marca)
        self.ui.click_incluir()
        self.ui.click_guardar()
        self.ui.esperar_success()

        # Captura de pantalla funcional
        capturar_evidencia(self.page, nombre_caso, "01_Alta_Inicial")

        # Validación en DB (Llamada limpia: solo el nombre)
        marca_db = repo_db.obtener_marca(nombre_marca)
        assert marca_db, f"Fallo Crítico: '{nombre_marca}' no se encontró en DB tras el alta."

        capturar_evidencia_sql(
            nombre_caso=nombre_caso,
            nombre_paso="01_SQL_Validacion_Alta_Marca",
            query=repo_db.SELECT_MARCA_BY_NOMBRE,
            params=[nombre_marca],
            resultado=f"REGISTRO_ENCONTRADO ID={marca_db['ID_MARCA']}"
        )

        logger.info(f"Confirmado en DB: ID {marca_db['ID_MARCA']}")

        # ==========================================================
        # 2. BAJA: Eliminación y validación dual (UI y DB)
        # ==========================================================
        logger.info(f"Paso 2: Eliminando marca '{nombre_marca}'")

        self.ui.buscar_marca_en_paginacion(nombre_marca)
        self.ui.seleccionar_marca_en_grid(nombre_marca)
        self.ui.click_eliminar()
        self.ui.click_guardar()
        self.ui.esperar_success()

        capturar_evidencia(self.page, nombre_caso, "02_Baja_y_Validacion_UI")

        # Validación de ausencia en DB (Llamada limpia: solo el nombre)
        check_baja = repo_db.obtener_marca(nombre_marca)
        assert not check_baja, f"Fallo: La marca '{nombre_marca}' persiste en DB tras eliminación."

        capturar_evidencia_sql(
            nombre_caso=nombre_caso,
            nombre_paso="02_SQL_Validacion_Baja_Marca",
            query=repo_db.SELECT_MARCA_BY_NOMBRE,
            params=[nombre_marca],
            resultado="SIN_REGISTROS"
        )

        return True
