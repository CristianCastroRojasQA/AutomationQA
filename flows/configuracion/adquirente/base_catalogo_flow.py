import time
from abc import ABC

from playwright.sync_api import expect
from utils.screenshots import capturar_evidencia
from utils.sql_evidence import capturar_evidencia_sql


class BaseCatalogoFlow(ABC):
    """
    Clase de flujo base genérica para catálogos (Marcas, Tecnologías).
    Coordina las acciones entre el Page Object y los datos de prueba con trazabilidad completa.
    """

    def __init__(self, page, ui):
        self.page = page
        self.ui = ui

        # -------------------------

    # Utilidades
    # -------------------------
    @staticmethod
    def generar_nombre_unico(prefijo="QA_Test") -> str:
        """Genera un nombre único con timestamp para evitar colisiones en DB."""
        return f"{prefijo}_{int(time.time())}"

    # ============================================================
    # FLUJOS - PRIORIDAD ALTA (HIGH SEVERITY)
    # ============================================================

    def flujo_alta_registro(self, valor: str, logger, nombre_caso: str):
        """Crea un registro, guarda cambios y verifica presencia en grilla."""
        logger.info(f"--- Iniciando Flujo: Alta de Registro ---")

        logger.info(f"Paso 1: Escribiendo valor '{valor}' en el campo principal")
        self.ui.escribir_valor(valor)
        capturar_evidencia(self.page, nombre_caso, "01_Digitacion_Valor")

        logger.info("Paso 2: Haciendo clic en 'Incluir' para agregar a la tabla local")
        self.ui.click_incluir()

        logger.info("Paso 3: Presionando 'Guardar' para persistencia en servidor")
        self.ui.click_guardar()

        logger.info("Paso 4: Esperando mensaje de confirmación (Success)")
        self.ui.esperar_alerta_exito()

        logger.info(f"Paso 5: Buscando '{valor}' en la grilla mediante paginación")
        encontrado = self.ui.buscar_en_paginacion(valor)

        resultado = "Exitosa" if encontrado else "Fallida"
        capturar_evidencia(self.page, nombre_caso, f"03_Busqueda_Grilla_{resultado}")
        logger.info(f"Fin de flujo: Alta {resultado}")
        return encontrado

    def flujo_validar_duplicado_exacto(self, valor: str, logger, nombre_caso: str):
        """Intenta dar de alta un valor existente y verifica el bloqueo."""
        logger.info(f"--- Iniciando Flujo: Validación Duplicado Exacto ---")

        logger.info(f"Pre-condición: Verificando si '{valor}' ya existe en el sistema")
        existe = self.ui.buscar_en_paginacion(valor)

        if not existe:
            logger.info(f"Registro '{valor}' no encontrado. Creándolo como base.")
            self.flujo_alta_registro(valor=valor, logger=logger, nombre_caso=nombre_caso)
            self.ui.buscar_en_paginacion(valor)

        ocurrencias_antes = self.ui.grid_cells().filter(has_text=valor).count()
        logger.info(f"Cantidad de coincidencias antes del intento: {ocurrencias_antes}")

        logger.info(f"Paso 1: Intentando incluir valor duplicado: '{valor}'")
        self.ui.escribir_valor(valor)
        self.ui.click_incluir()

        logger.info("Paso 2: Esperando alerta de advertencia (Warning Duplicado)")
        self.ui.esperar_alerta_duplicado()

        exito_visible = self.ui.es_alerta_exito_visible()
        capturar_evidencia(self.page, nombre_caso, "01_Advertencia_Duplicado_Visible")

        ocurrencias_despues = self.ui.grid_cells().filter(has_text=valor).count()
        logger.info(f"Cantidad de coincidencias después del intento: {ocurrencias_despues}")

        es_valido = not exito_visible and (ocurrencias_antes == ocurrencias_despues)
        logger.info(f"Resultado de validación duplicado: {'Correcto' if es_valido else 'Incorrecto'}")
        return es_valido

    def flujo_validar_duplicado_logico(self, valor: str, logger, nombre_caso: str):
        """Intenta ingresar variantes (minúsculas/espacios) de un registro existente."""
        logger.info(f"--- Iniciando Flujo: Validación Duplicado Lógico ---")

        if not self.ui.buscar_en_paginacion(valor):
            logger.info(f"Creando registro base '{valor}' para pruebas de variantes")
            self.flujo_alta_registro(valor, logger, nombre_caso)
            self.page.reload()

        variantes = [valor.lower(), f" {valor} ", valor.upper() if valor != valor.upper() else f"{valor}  "]

        for i, v in enumerate(variantes):
            logger.info(f"Variante {i + 1}: Probando con '{v}'")
            self.ui.escribir_valor(v)
            self.ui.click_incluir()

            logger.info(f"Esperando bloqueo para variante '{v}'")
            self.ui.esperar_alerta_duplicado()
            capturar_evidencia(self.page, nombre_caso, f"0{i + 1}_Bloqueo_Variante")

            assert not self.ui.es_alerta_exito_visible(), f"Error Crítico: Se guardó la variante '{v}'"

        logger.info("Todas las variantes fueron bloqueadas correctamente por el sistema.")
        return self.ui.buscar_en_paginacion(valor)

    def flujo_eliminar_registro(self, valor: str, logger, nombre_caso: str):
        """Localiza un registro, lo elimina y confirma persistencia."""
        logger.info(f"--- Iniciando Flujo: Eliminación de Registro ---")

        if not self.ui.buscar_en_paginacion(valor):
            logger.info(f"El registro '{valor}' no existe. Creándolo para proceder con la eliminación.")
            self.flujo_alta_registro(valor, logger, nombre_caso)
            self.ui.buscar_en_paginacion(valor)

        logger.info(f"Paso 1: Seleccionando '{valor}' en el grid")
        self.ui.seleccionar_registro_en_grid(valor)
        capturar_evidencia(self.page, nombre_caso, "01_Registro_Seleccionado")

        logger.info("Paso 2: Verificando habilitación de botón Eliminar y ejecutando click")
        assert not self.ui.es_boton_eliminar_deshabilitado(), "El botón Eliminar está deshabilitado."
        self.ui.click_eliminar()

        logger.info("Paso 3: Verificando remoción visual en el grid local")
        expect(self.ui.grid_cells().filter(has_text=valor)).to_have_count(0)

        logger.info("Paso 4: Guardando cambios para confirmar baja en servidor")
        self.ui.click_guardar()
        self.ui.esperar_alerta_exito()

        logger.info("Paso 5: Verificando ausencia definitiva del registro")
        todavia_existe = self.ui.buscar_en_paginacion(valor)
        capturar_evidencia(self.page, nombre_caso, "03_Confirmacion_Eliminacion")

        return not todavia_existe

    # ============================================================
    # FLUJOS - PRIORIDAD MEDIA (MEDIUM SEVERITY / SEGURIDAD)
    # ============================================================

    def flujo_validar_no_success_ante_error(self, logger, nombre_caso: str):
        """Verifica que el sistema NO muestre éxito si hay errores de validación."""
        logger.info("--- Iniciando Flujo: Validación Ausencia de Success ante Error ---")

        logger.info("Paso 1: Provocando error de validación (dejando campo vacío)")
        self.ui.escribir_valor("")
        self.ui.click_incluir()

        logger.info("Paso 2: Intentando guardar con el formulario inválido")
        self.ui.click_guardar()

        exito_visible = self.ui.es_alerta_exito_visible()
        logger.info(f"¿Se visualiza mensaje de éxito?: {exito_visible}")

        capturar_evidencia(self.page, nombre_caso, "01_Verificacion_Ausencia_Success")
        return not exito_visible

    def flujo_verificar_inclusion_visual_sin_guardar(self, valor: str, logger, nombre_caso: str):
        """Valida que el registro aparezca en grilla tras 'Incluir' sin 'Guardar'."""
        logger.info("--- Iniciando Flujo: Verificación de Inclusión Visual Temporal ---")

        logger.info(f"Escribiendo '{valor}' e incluyendo en grilla local")
        self.ui.escribir_valor(valor)
        self.ui.click_incluir()

        logger.info("Verificando visibilidad del registro en el grid antes de guardar")
        expect(self.ui.grid_cells().filter(has_text=valor).first).to_be_visible()
        capturar_evidencia(self.page, nombre_caso, "02_Inclusion_Visual_Temporal")

        logger.info("Cancelando operación para limpiar cambios locales")
        self.ui.click_cancelar()
        return True

    # ============================================================
    # FLUJOS - PRIORIDAD BAJA (LOW SEVERITY / UI)
    # ============================================================

    def flujo_validar_longitud_maxima(self, logger, nombre_caso: str):
        """Verifica el truncamiento del texto según el límite del input."""
        logger.info("--- Iniciando Flujo: Validación de Longitud Máxima ---")

        max_len = int(self.ui.INPUT_MAX_LENGTH)
        texto_largo = "A" * (max_len + 5)

        logger.info(f"Intentando ingresar {len(texto_largo)} caracteres (Límite esperado: {max_len})")
        self.ui.escribir_valor(texto_largo)

        valor_real = self.ui.obtener_valor_input()
        longitud_real = len(valor_real)
        logger.info(f"Longitud real en el campo tras entrada: {longitud_real}")

        capturar_evidencia(self.page, nombre_caso, f"01_Validacion_Longitud_{longitud_real}")
        return longitud_real == max_len

    def flujo_validar_persistencia_reload(self, valor: str, logger, nombre_caso: str):
        """Valida que el dato persista tras un refresco de página (F5)."""
        logger.info("--- Iniciando Flujo: Validación de Persistencia tras F5 ---")

        self.flujo_alta_registro(valor, logger, nombre_caso)

        logger.info("Ejecutando recarga de página (browser reload)")
        self.ui.recargar_pagina()

        logger.info(f"Buscando el registro '{valor}' post-recarga")
        existe = self.ui.buscar_en_paginacion(valor)

        capturar_evidencia(self.page, nombre_caso, "02_Persistencia_Post_Reload")
        return existe

    def flujo_validar_campo_obligatorio(self, logger, nombre_caso: str):
        """Verifica el bloqueo de inclusión y guardado con campo vacío."""
        logger.info("--- Iniciando Flujo: Validación de Campo Obligatorio ---")

        cant_inicial = self.ui.obtener_conteo_grid()
        logger.info(f"Conteo inicial de registros: {cant_inicial}")

        logger.info("Intentando incluir un valor vacío")
        self.ui.escribir_valor("")
        self.ui.click_incluir()

        error_ui = self.ui.es_input_invalido() or self.ui.msg_error_campo().is_visible()
        bloqueo_grilla = (self.ui.obtener_conteo_grid() == cant_inicial)

        logger.info(f"¿Error UI visible?: {error_ui} | ¿Grilla bloqueada?: {bloqueo_grilla}")

        self.ui.click_guardar()
        permite_guardar = self.ui.es_alerta_exito_visible()

        logger.info(f"¿Se permitió guardar con campo vacío?: {permite_guardar}")
        capturar_evidencia(self.page, nombre_caso, "02_Bloqueo_Campo_Obligatorio")

        return error_ui and bloqueo_grilla and not permite_guardar

    # ============================================================
    # E2E - AUDITORÍA BASE DE DATOS (HIGH SEVERITY)
    # ============================================================

    def flujo_ciclo_completo_con_db(self, valor: str, logger, nombre_caso: str, repo_db, query_sql: str):
        """Ejecuta ciclo Alta/Baja con validación directa en SQL."""
        logger.info("--- Iniciando Flujo E2E: Ciclo Completo con Auditoría DB ---")

        logger.info(f"Paso 1: Alta del registro '{valor}'")
        self.ui.escribir_valor(valor)
        self.ui.click_incluir()
        self.ui.click_guardar()
        self.ui.esperar_alerta_exito()

        logger.info("Paso 2: Consultando Base de Datos para confirmar creación")
        registro_db = repo_db.obtener_registro(valor)
        assert registro_db, f"Error Crítico: '{valor}' no se insertó en la base de datos."

        capturar_evidencia_sql(nombre_caso, "01_SQL_Alta", query_sql, [valor], "REGISTRO_ENCONTRADO")

        logger.info(f"Paso 3: Eliminación del registro '{valor}'")
        self.ui.buscar_en_paginacion(valor)
        self.ui.seleccionar_registro_en_grid(valor)
        self.ui.click_eliminar()
        self.ui.click_guardar()
        self.ui.esperar_alerta_exito()

        logger.info("Paso 4: Consultando Base de Datos para confirmar eliminación")
        assert repo_db.esperar_no_existencia(valor), f"Error Crítico: '{valor}' aún persiste en la DB."

        capturar_evidencia_sql(nombre_caso, "02_SQL_Baja", query_sql, [valor], "SIN_REGISTROS")

        logger.info("Flujo E2E finalizado exitosamente.")
        return True
