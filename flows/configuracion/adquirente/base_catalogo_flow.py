import time
from abc import ABC

from utils.bug_reporter import BugReporter
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

    def flujo_alta_registro(self, valor: str, logger, nombre_caso: str) -> bool:
        """
        Crea un registro, guarda cambios y verifica presencia en grilla.
        Certifica la falla si el registro no persiste o el sistema miente en el éxito.
        """
        logger.info(f"=== INICIO FLUJO: ALTA DE REGISTRO [{valor}] ===")

        # Paso 1: Digitación
        logger.info("Paso 1: Digitación del valor en el input")
        self.ui.escribir_valor(valor)
        capturar_evidencia(self.page, nombre_caso, "01_Digitacion_Valor")

        if self.ui.es_input_invalido():
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Input_Invalido",
                                         f"El sistema marca como inválido el valor: {valor}")

        # Paso 2: Incluir en grilla local
        logger.info("Paso 2: Click en 'Incluir' para agregar a la tabla local")
        self.ui.click_incluir()

        logger.info("Paso 2.1: Validando inclusión del registro en la grilla local")
        incluido_local = self.ui.buscar_en_paginacion(valor)

        capturar_evidencia(self.page, nombre_caso,
                           "02_Inclusion_Local_OK" if incluido_local else "02_INCLUSION_LOCAL_FALLA")

        if not incluido_local:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Inclusion_Fallida",
                                         f"El sistema no incluyó localmente el registro: {valor}")

        # Paso 3: Guardar
        logger.info("Paso 3: Click en 'Guardar' para persistencia en servidor")
        self.ui.click_guardar()

        # Paso 4: Confirmación backend
        logger.info("Paso 4: Esperando mensaje de éxito del sistema")
        self.ui.esperar_alerta_exito()
        capturar_evidencia(self.page, nombre_caso, "03_Mensaje_Exito")

        # Paso 5: Validación post‑persistencia (CRÍTICA)
        logger.info(f"Paso 5: Buscando '{valor}' en la grilla mediante paginación")
        encontrado = self.ui.buscar_en_paginacion(valor)

        capturar_evidencia(self.page, nombre_caso,
                           "04_Persistencia_OK" if encontrado else "04_PERSISTENCIA_FALLA")

        if not encontrado:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Persistencia_Final_Fail",
                                         f"El sistema mostró éxito, pero el registro NO ES VISIBLE tras guardar.")

        logger.info(f"=== FIN FLUJO: ALTA EXITOSA [{valor}] ===")
        return True

    def flujo_validar_campo_obligatorio(self, logger, nombre_caso: str) -> bool:
        """
        Verifica el bloqueo de inclusión y guardado con campo vacío.
        Certifica la falla si el sistema no valida la obligatoriedad.
        """
        logger.info("=== INICIO FLUJO: VALIDAR CAMPO OBLIGATORIO ===")

        # Paso 0: Conteo inicial
        cant_inicial = self.ui.obtener_conteo_grid()
        logger.info(f"Estado inicial - Conteo grilla: {cant_inicial}")

        # Paso 1: Intento de inclusión con valor vacío
        logger.info("Paso 1: Intentando incluir un valor vacío")
        self.ui.escribir_valor("")
        self.ui.click_incluir()

        # Validamos estado de la UI y de la grilla
        error_ui = self.ui.es_input_invalido() or self.ui.msg_error_campo.is_visible()
        bloqueo_grilla = (self.ui.obtener_conteo_grid() == cant_inicial)

        capturar_evidencia(self.page, nombre_caso, "01_Intento_Incluir_Vacio")

        if not error_ui:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "No_Valida_Vacio",
                                         "El sistema no marca el input como inválido al estar vacío.")

        if not bloqueo_grilla:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Vacio_En_Grilla",
                                         "BUG: Se agregó una fila vacía a la grilla local.")

        # Paso 2: Intento de guardado
        logger.info("Paso 2: Intentando Guardar con el error presente")
        self.ui.click_guardar()

        permite_guardar = self.ui.es_alerta_exito_visible()
        capturar_evidencia(self.page, nombre_caso, "02_Resultado_Guardar_Vacio")

        if permite_guardar:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Guardado_Invalido_Permitido",
                                         "CRÍTICO: El sistema permitió guardar y mostró éxito con campos vacíos.")

        logger.info("=== FIN FLUJO: VALIDACIÓN CORRECTA (Bloqueo exitoso) ===")
        return True

    def flujo_validar_duplicado_exacto(self, valor: str, logger, nombre_caso: str) -> bool:
        """
        Intenta dar de alta un valor existente y verifica que el sistema bloquee la duplicidad.
        Certifica la falla si el sistema permite el ingreso del mismo valor dos veces.
        """
        logger.info(f"=== INICIO FLUJO: VALIDAR DUPLICADO EXACTO [{valor}] ===")

        # Paso 1: Creación del registro base
        logger.info("Paso 1: Creando registro base para validación de duplicado")
        self.flujo_alta_registro(valor=valor, logger=logger, nombre_caso=nombre_caso)

        # Paso 2: Verificación de estado inicial
        logger.info("Paso 2: Verificando que el registro base sea visible y contando grilla")
        existe = self.ui.buscar_en_paginacion(valor)

        if not existe:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Registro_Base_No_Visible",
                                         f"El registro base '{valor}' no aparece tras su creación.")

        conteo_inicial = self.ui.obtener_conteo_grid()
        logger.info(f"Conteo inicial de registros: {conteo_inicial}")

        # Paso 3: Intento de inclusión duplicada
        logger.info(f"Paso 3: Intentando incluir duplicado exacto del valor '{valor}'")
        self.ui.escribir_valor(valor)
        self.ui.click_incluir()

        # Paso 4: Validación de advertencia
        logger.info("Paso 4: Esperando alerta de advertencia por duplicado")
        self.ui.esperar_alerta_duplicado()
        capturar_evidencia(self.page, nombre_caso, "01_Advertencia_Duplicado")

        # Paso 5: Verificación de integridad de la grilla
        logger.info(f"Paso 5: Validando que el conteo de la grilla no haya variado. Resultado:{conteo_inicial}")
        conteo_final = self.ui.obtener_conteo_grid()

        capturar_evidencia(self.page, nombre_caso,
                           "02_Conteo_Duplicado_OK" if conteo_final == conteo_inicial else "02_CONTEO_DUPLICADO_FALLA")

        if conteo_final != conteo_inicial:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Grilla_Modificada",
                                         f"BUG: El conteo cambió ({conteo_inicial} -> {conteo_final}) tras intentar incluir un duplicado.")

        logger.info(f"=== FIN FLUJO: DUPLICADO BLOQUEADO CORRECTAMENTE [{valor}] ===")
        return True

    def flujo_validar_duplicado_logico(self, valor: str, logger, nombre_caso: str) -> bool:
        """
        Intenta ingresar variantes (minúsculas, mayúsculas y espacios) de un registro existente.
        Certifica la falla si el sistema permite el ingreso de duplicados por falta de normalización.
        """
        logger.info(f"=== INICIO FLUJO: VALIDAR DUPLICADO LÓGICO [{valor}] ===")

        # Paso 1: Creación del registro base
        logger.info("Paso 1: Creando registro base para validación de duplicado")
        self.flujo_alta_registro(valor=valor, logger=logger, nombre_caso=nombre_caso)

        # Paso 2: Verificación de estado inicial
        logger.info("Paso 2: Verificando visibilidad del registro base y contando grilla")
        existe = self.ui.buscar_en_paginacion(valor)

        if not existe:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Registro_Base_No_Visible",
                                         f"El registro base '{valor}' no aparece tras su creación.")

        conteo_inicial = self.ui.obtener_conteo_grid()
        logger.info(f"Conteo inicial de registros: {conteo_inicial}")

        # Paso 3: Definición de variantes lógicas
        variantes = [
            valor.lower(),
            valor.upper(),
            f" {valor} ",
            f"{valor}  ",
            f" {valor.lower()} ",
        ]
        logger.info(f"Variantes a validar: {variantes}")

        # Paso 4: Pruebas iterativas de variantes
        for idx, variante in enumerate(variantes, start=1):
            logger.info(f"Paso 4.{idx}: Probando variante '{variante}'")

            self.ui.escribir_valor(variante)
            self.ui.click_incluir()

            logger.info(f"Esperando alerta de duplicado para la variante: '{variante}'")
            self.ui.esperar_alerta_duplicado()

            capturar_evidencia(self.page, nombre_caso, f"0{idx}_Variante_{idx}_Bloqueada")

            # Paso 5: Verificación de integridad de la grilla por variante
            conteo_actual = self.ui.obtener_conteo_grid()
            logger.info(f"Conteo tras variante '{variante}': {conteo_actual}")

            if conteo_actual != conteo_inicial:
                BugReporter.certificar_falla(self.page, logger, nombre_caso, f"Variante_{idx}_Falla",
                                             f"BUG: La variante '{variante}' se saltó la validación y alteró la grilla.")

        logger.info("=== FIN FLUJO: TODAS LAS VARIANTES BLOQUEADAS CORRECTAMENTE ===")
        return True

    def flujo_eliminar_registro(self, valor: str, logger, nombre_caso: str) -> bool:
        """
        Localiza un registro, realiza la baja lógica/física y confirma la persistencia del borrado.
        Certifica la falla si el registro permanece en el sistema tras el guardado.
        NO usar este flujo para eliminar registros preexistentes.
        """
        logger.info(f"=== INICIO FLUJO: ELIMINACIÓN DE REGISTRO [{valor}] ===")

        # Paso 1: Creación del registro base
        logger.info("Paso 1: Creando registro previo para validar su eliminación")
        self.flujo_alta_registro(valor=valor, logger=logger, nombre_caso=nombre_caso)

        if not self.ui.buscar_en_paginacion(valor):
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Registro_No_Visible",
                                         f"El registro '{valor}' no aparece tras su creación.")

        # Paso 2: Selección y verificación de botón
        logger.info(f"Paso 2: Seleccionando '{valor}' y verificando botón de acción")
        self.ui.seleccionar_registro_en_grid(valor)
        capturar_evidencia(self.page, nombre_caso, "01_Registro_Seleccionado")

        if not self.ui.es_boton_eliminar_habilitado():
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Boton_Eliminar_Blocked",
                                         f"El botón 'Eliminar' quedó deshabilitado al seleccionar el registro.")

        # Paso 3: Eliminación local
        logger.info("Paso 3: Ejecutando eliminación local (remoción de fila)")
        self.ui.click_eliminar()
        capturar_evidencia(self.page, nombre_caso, "02_Registro_Eliminado_Local")

        # Paso 4: Persistencia del borrado (Guardar)
        logger.info("Paso 4: Click en 'Guardar' para confirmar la baja en el backend")
        self.ui.click_guardar()
        self.ui.esperar_alerta_exito()
        capturar_evidencia(self.page, nombre_caso, "03_Mensaje_Exito_Baja")

        # Paso 5: Verificación final de ausencia
        logger.info("Paso 5: Verificando ausencia definitiva mediante búsqueda en paginación")
        todavia_existe = self.ui.buscar_en_paginacion(valor)

        capturar_evidencia(self.page, nombre_caso,
                           "04_Confirmacion_Baja_OK" if not todavia_existe else "04_BAJA_FALLIDA")

        if todavia_existe:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Baja_No_Persistida",
                                         f"BUG: El registro '{valor}' sigue visible tras confirmar la eliminación.")

        logger.info(f"=== FIN FLUJO: ELIMINACIÓN EXITOSA [{valor}] ===")
        return True

    def flujo_validar_guardar_con_error_no_persistente(self, logger, nombre_caso: str) -> bool:
        """
        Valida que, aunque el sistema muestre mensaje de éxito,
        NO persista ningún registro cuando el formulario es inválido.
        """
        logger.info("=== INICIO FLUJO: GUARDAR CON ERROR SIN PERSISTENCIA ===")

        # Paso 1: Provocar error de validación
        logger.info("Paso 1: Provocando error (campo obligatorio vacío)")
        self.ui.escribir_valor("")
        self.ui.click_incluir()

        if not self.ui.es_input_invalido():
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Formulario_No_Invalido",
                                         "El formulario no quedó marcado como inválido estando vacío.")

        capturar_evidencia(self.page, nombre_caso, "01_Formulario_Invalido_OK")

        # Paso 2: Guardar estado inicial de la grilla
        logger.info("Paso 2: Obteniendo conteo inicial de la grilla para comparar")
        conteo_inicial = self.ui.obtener_conteo_grid()
        logger.info(f"Conteo inicial: {conteo_inicial}")

        # Paso 3: Intentar guardar
        logger.info("Paso 3: Intentando guardar con formulario inválido")
        self.ui.click_guardar()
        self.ui.esperar_alerta_exito()

        capturar_evidencia(self.page, nombre_caso, "02_Guardar_Invalido_Con_Success")

        # Paso 4: Validar NO persistencia
        logger.info("Paso 4: Validando que el conteo de la grilla no haya variado")
        conteo_final = self.ui.obtener_conteo_grid()
        logger.info(f"Conteo final: {conteo_final} (Esperado: {conteo_inicial})")

        capturar_evidencia(self.page, nombre_caso,
                           "03_Persistencia_Bloqueada_OK" if conteo_final == conteo_inicial else "03_PERSISTENCIA_INDEBIDA_FALLA")

        if conteo_final != conteo_inicial:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Persistencia_Indebida",
                                         f"BUG: Se persistió un registro ({conteo_inicial} -> {conteo_final}) pese a tener errores de validación.")

        logger.info("=== FIN FLUJO: VALIDACIÓN SIN PERSISTENCIA EXITOSA ===")
        return True

    # ============================================================
    # FLUJOS - PRIORIDAD MEDIA (MEDIUM SEVERITY / SEGURIDAD)
    # ============================================================

    def flujo_verificar_inclusion_visual_sin_guardar(self, logger, nombre_caso: str) -> bool:
        """
        Valida que un registro incluido SIN guardar aparezca visualmente en la grilla,
        realizando la cancelación como paso final para limpiar el estado.
        """
        logger.info("=== INICIO FLUJO: INCLUSIÓN VISUAL SIN GUARDAR ===")

        # Paso 0: Generar valor único
        valor = self.generar_nombre_unico("Marca_Temporal")
        logger.info(f"Valor temporal generado: '{valor}'")

        # Paso 1: Obtener estado inicial
        conteo_inicial = self.ui.obtener_conteo_grid()
        logger.info(f"Conteo inicial de la grilla: {conteo_inicial}")

        # Paso 2: Incluir sin guardar
        logger.info("Paso 2: Incluyendo registro en la tabla local (sin presionar Guardar)")
        self.ui.escribir_valor(valor)
        self.ui.click_incluir()

        # Paso 3: Validar que el registro APARECE visualmente
        if not self.ui.buscar_en_paginacion(valor):
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Inclusion_Local_Fail",
                                         f"El registro '{valor}' no apareció visualmente tras presionar 'Incluir'.")

        capturar_evidencia(self.page, nombre_caso, "01_Inclusion_Visual_Temporal_OK")

        # Paso 4: Validar el conteo con el registro presente
        logger.info("Paso 4: Validando el conteo con el registro temporal presente")
        conteo_con_item = self.ui.obtener_conteo_grid()
        logger.info(f"Conteo actual: {conteo_con_item}")

        # Paso 5: Verificación de presencia antes de salir
        logger.info(f"Paso 5: Verificando que '{valor}' es visible en la grilla")
        existe_en_grilla = self.ui.buscar_en_paginacion(valor)

        if not existe_en_grilla:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Error_Visibilidad",
                                         f"El registro '{valor}' desapareció antes de finalizar.")

        # Paso 6: Retorno
        logger.info("Paso 6: Presionando 'Cancelar' para descartar cambios y limpiar")
        self.ui.click_cancelar()

        # Sincronización mínima para que el cierre del test no choque con el refresco de la grilla
        self.page.wait_for_load_state("networkidle")
        capturar_evidencia(self.page, nombre_caso, "02_Cancelacion_Ejecutada_OK")

        logger.info("=== FIN FLUJO: INCLUSIÓN VISUAL VALIDADA Y CANCELADA EXITOSAMENTE ===")
        return True

    def flujo_validar_boton_eliminar_sin_seleccion(self, logger, nombre_caso: str) -> bool:
        """
        Verifica que al ingresar a la pantalla, sin seleccionar ningún registro,
        el botón 'Eliminar' se encuentre deshabilitado por defecto.
        """
        logger.info("=== INICIO FLUJO: BOTÓN ELIMINAR SIN SELECCIÓN ===")

        # Paso 1: Verificar estado inicial del botón Eliminar
        logger.info("Paso 1: Validando que el botón 'Eliminar' esté deshabilitado por defecto")

        # Capturamos evidencia antes de la validación para mostrar el estado real de la UI
        capturar_evidencia(self.page, nombre_caso, "01_Estado_Inicial_Boton_Eliminar")

        # Validación de seguridad: el botón NO debe estar habilitado
        boton_habilitado = self.ui.es_boton_eliminar_habilitado()

        if boton_habilitado:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Boton_Eliminar_Habilitado_Error",
                                         "BUG: El botón 'Eliminar' está habilitado sin haber seleccionado ningún registro de la grilla.")

        logger.info("Validación correcta: el botón se encuentra bloqueado como se esperaba.")

        logger.info("=== FIN FLUJO: BOTÓN ELIMINAR SIN SELECCIÓN EXITOSO ===")
        return True

    # ============================================================
    # FLUJOS - PRIORIDAD BAJA (LOW SEVERITY / UI)
    # ============================================================

    def flujo_validar_longitud_maxima(self, logger, nombre_caso: str) -> bool:
        """
        Valida que el campo de texto aplique correctamente el límite máximo
        de caracteres definido en el atributo del input (truncamiento).
        """
        logger.info("=== INICIO FLUJO: VALIDACIÓN LONGITUD MÁXIMA ===")

        # Paso 1: Obtener configuración del componente
        max_len = int(self.ui.INPUT_MAX_LENGTH)
        logger.info(f"Longitud máxima permitida en el input: {max_len}")

        texto_largo = "A" * (max_len + 5)
        logger.info(f"Intentando ingresar {len(texto_largo)} caracteres (excede el límite)")

        # Paso 2: Ingresar texto excedente
        logger.info(f"Paso 2: Digitando valor de longitud {len(texto_largo)}")
        self.ui.escribir_valor(texto_largo)
        capturar_evidencia(self.page, nombre_caso, "01_Texto_Largo_Ingresado")

        # Paso 3: Obtener valor real y validar truncamiento
        logger.info("Paso 3: Verificando el valor final contenido en el input")
        valor_real = self.ui.obtener_valor_input()
        longitud_real = len(valor_real)

        logger.info(f"Longitud real en UI: {longitud_real} (Esperado: {max_len})")

        capturar_evidencia(self.page, nombre_caso,
                           f"02_Validacion_Len_{longitud_real}_OK" if longitud_real == max_len else "02_FALLA_LONGITUD")

        # Paso 4: Certificación de la regla de negocio
        if longitud_real != max_len:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Longitud_Maxima_No_Respetada",
                                         f"El input permitió {longitud_real} caracteres, ignorando el máximo de {max_len}.")

        logger.info("Validación correcta: el sistema truncó el texto al límite máximo permitido.")

        logger.info("=== FIN FLUJO: VALIDACIÓN LONGITUD MÁXIMA EXITOSA ===")
        return True

    def flujo_validar_persistencia_reload(self, valor: str, logger, nombre_caso: str) -> bool:
        """
        Valida que un registro persistido permanezca visible tras un refresco
        completo de la página (equivalente a F5).
        """
        logger.info(f"=== INICIO FLUJO: PERSISTENCIA TRAS RELOAD [{valor}] ===")

        # Paso 1: Crear y persistir el registro
        logger.info("Paso 1: Creando y guardando registro inicial")
        self.flujo_alta_registro(valor=valor, logger=logger, nombre_caso=nombre_caso)

        # Paso 2: Recargar la página (F5)
        logger.info("Paso 2: Ejecutando recarga de página (browser reload / F5)")
        self.ui.recargar_pagina()
        capturar_evidencia(self.page, nombre_caso, "01_Pagina_Recargada")

        # Paso 3: Verificar persistencia post‑reload
        logger.info(f"Paso 3: Verificando que el registro '{valor}' persista en la grilla")
        existe = self.ui.buscar_en_paginacion(valor)

        capturar_evidencia(self.page, nombre_caso,
                           "02_Persistencia_Reload_OK" if existe else "02_PERSISTENCIA_RELOAD_FALLA")

        if not existe:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Persistencia_Post_Reload_Fallida",
                                         f"BUG: El registro '{valor}' desapareció tras recargar la página (F5).")

        logger.info("Validación correcta: el registro se mantiene íntegro tras la recarga.")

        logger.info("=== FIN FLUJO: PERSISTENCIA TRAS RELOAD EXITOSO ===")
        return True

    def flujo_validar_texto_mensaje_success(self, nombre: str, logger, nombre_caso: str) -> bool:
        """
        Crea un registro y valida que el texto del mensaje de éxito
        sea EXACTAMENTE el definido por los requerimientos del sistema.
        """
        logger.info(f"=== INICIO FLUJO: VALIDACIÓN TEXTO MENSAJE SUCCESS [{nombre}] ===")

        # Paso 0: Definición del mensaje esperado (Requerimiento)
        mensaje_esperado = self.ui.SUCCESS_TEXT
        logger.info(f"Mensaje esperado por contrato: '{mensaje_esperado}'")

        # Paso 1: Alta del registro para disparar el mensaje
        logger.info(f"Paso 1: Creando registro '{nombre}' para generar la alerta")
        self.ui.escribir_valor(nombre)
        self.ui.click_incluir()
        self.ui.click_guardar()

        # Paso 2: Capturar el mensaje de éxito en la UI
        logger.info("Paso 2: Esperando y capturando el texto real de la alerta")
        self.ui.esperar_alerta_exito()
        texto_real = self.ui.obtener_texto_alerta_exito()

        logger.info(f"Texto capturado en pantalla: '{texto_real}'")
        capturar_evidencia(self.page, nombre_caso, "01_Validacion_Texto_Success")

        # Paso 3: Validación estricta del contenido
        logger.info("Paso 3: Verificando coincidencia exacta de caracteres")

        coincide = (texto_real == mensaje_esperado)

        capturar_evidencia(self.page, nombre_caso,
                           "02_Texto_Correcto_OK" if coincide else "02_TEXTO_ERRONEO_FALLA")

        if not coincide:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Texto_Success_Incorrecto",
                                         f"ERROR DE REQUERIMIENTO: El texto no coincide.\nEsperado: '{mensaje_esperado}'\nObtenido: '{texto_real}'")

        logger.info("Validación correcta: el mensaje de éxito cumple con el estándar requerido.")

        logger.info("=== FIN FLUJO: VALIDACIÓN TEXTO SUCCESS EXITOSA ===")
        return True

        # ============================================================
        # E2E - AUDITORÍA BASE DE DATOS (HIGH SEVERITY)
        # ============================================================

    def flujo_validar_texto_mensaje_warning(self, nombre: str, logger, nombre_caso: str) -> bool:
        """
        Crea un registro y valida que el texto del mensaje de warning
        sea EXACTAMENTE el definido por los requerimientos del sistema.
        """
        logger.info(f"=== INICIO FLUJO: VALIDACIÓN TEXTO MENSAJE WARNING [{nombre}] ===")

        # Paso 0: Mensaje esperado definido por el contrato del POM
        mensaje_esperado = self.ui.WARNING_DUPLICADO_TEXT
        logger.info(f"Mensaje warning esperado por contrato: '{mensaje_esperado}'")

        # Paso 1: Alta base + disparo del warning (duplicado)
        logger.info(f"Paso 1: Creando registro y provocando duplicado '{nombre}'")
        self.ui.escribir_valor(nombre)
        self.ui.click_incluir()
        self.ui.click_guardar()

        # Intento duplicado para disparar el warning
        self.ui.escribir_valor(nombre)
        self.ui.click_incluir()

        # Paso 2: Esperar y capturar el warning
        logger.info("Paso 2: Esperando y capturando el texto real del warning")
        self.ui.esperar_alerta_duplicado()
        texto_real = self.ui.obtener_texto_alerta_warning()

        logger.info(f"Texto warning capturado: '{texto_real}'")
        capturar_evidencia(self.page, nombre_caso, "01_Validacion_Texto_Warning")

        # Paso 3: Validación estricta
        if texto_real != mensaje_esperado:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Texto_Warning_Incorrecto", (
                "ERROR DE REQUERIMIENTO: El texto del warning no coincide.\n"
                f"Esperado: '{mensaje_esperado}'\n"
                f"Obtenido: '{texto_real}'"
            ))

        logger.info("Validación correcta: el mensaje warning cumple con el estándar requerido.")
        logger.info("=== FIN FLUJO: VALIDACIÓN TEXTO WARNING EXITOSA ===")
        return True

    def flujo_validar_texto_error_eliminar_con_relacion(self, logger, nombre_caso: str, repo_db,
                                                        query_sql: str) -> bool:
        """
        Valida que al intentar eliminar una marca que tiene relaciones activas en la DB,
        el sistema bloquee la acción y muestre el mensaje de error definido por contrato.
        """
        logger.info("=== INICIO FLUJO: VALIDACIÓN ERROR ELIMINAR CON RELACIÓN ===")

        # Paso 0: Obtener marca con relación desde DB
        logger.info("Paso 0: Consultando DB para obtener una marca con dependencia de modelos")
        registro_db = repo_db.obtener_registro_con_relacion()

        nombre_registro = registro_db["NOMBRE_REGISTRO"]
        id_registro = registro_db["ID_REGISTRO"]
        tipo = registro_db.get("TIPO", "REGISTRO")

        logger.info(f"{tipo} obtenida con relación: '{nombre_registro}' (ID={id_registro})")

        # Auditoría inicial en base de datos
        capturar_evidencia_sql(nombre_caso, f"00_SQL_{tipo}Verificacion_Relacion", query_sql, params=None,
                               resultado=registro_db)

        # Mensaje esperado según contrato del componente UI
        mensaje_esperado = self.ui.ERROR_ELIMINAR_RELACION_TEXT
        logger.info(f"Mensaje de error esperado por contrato: '{mensaje_esperado}'")

        # Paso 1: Seleccionar la marca en UI
        logger.info(f"Paso 1: Buscando y seleccionando el registro '{nombre_registro}' en la grilla")
        self.ui.preparar_registro_para_eliminacion(nombre_registro)
        capturar_evidencia(self.page, nombre_caso, "01_Registro_Seleccionada")

        # Paso 2: Intentar eliminar la marca
        logger.info(f"Paso 2: Intentando ejecutar eliminación de '{nombre_registro}' con relación activa")
        self.ui.click_eliminar()
        self.ui.click_guardar()  # Nota: Cambié cancelar por guardar para que realmente intente procesar

        # Paso 3: Esperar y capturar alerta de error
        logger.info("Paso 3: Esperando visibilidad del mensaje de error por integridad referencial")
        self.ui.esperar_alerta_error_relacion()

        texto_real = self.ui.obtener_texto_alerta_error_relacion()
        logger.info(f"Texto de error capturado: '{texto_real}'")

        capturar_evidencia(self.page, nombre_caso, "02_Alert_Error_Relacion_Visible")

        # Paso 4: Validación estricta del mensaje de error
        logger.info("Paso 4: Verificando coincidencia exacta del texto de error")

        coincide = (texto_real == mensaje_esperado)

        capturar_evidencia(self.page, nombre_caso,
                           "03_Validacion_Error_OK" if coincide else "03_TEXTO_ERROR_FALLA")

        if not coincide:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Texto_Error_Relacion_Incorrecto",
                                         f"ERROR DE REQUERIMIENTO: El texto no coincide.\nEsperado: '{mensaje_esperado}'\nObtenido: '{texto_real}'")

        logger.info("Validación correcta: el sistema bloqueó la eliminación y mostró el mensaje esperado.")

        logger.info("=== FIN FLUJO: VALIDACIÓN ERROR ELIMINAR CON RELACIÓN EXITOSA ===")
        return True

    # ============================================================
    # E2E - AUDITORÍA BASE DE DATOS (HIGH SEVERITY)
    # ============================================================

    def flujo_ciclo_completo_con_db(self, valor: str, logger, nombre_caso: str, repo_db, query_sql: str) -> bool:
        """
        Flujo E2E: Alta y Baja del MISMO registro con validación directa en Base de Datos.
        Certifica la persistencia real y el borrado físico/lógico del dato en el backend.
        """
        logger.info(f"=== INICIO FLUJO E2E: CICLO COMPLETO CON AUDITORÍA DB [{valor}] ===")

        # Paso 1: Alta del registro desde UI
        logger.info("Paso 1: Ejecutando alta del registro desde la interfaz")
        self.ui.escribir_valor(valor)
        self.ui.click_incluir()
        self.ui.click_guardar()
        self.ui.esperar_alerta_exito()

        capturar_evidencia(self.page, nombre_caso, "01_UI_Alta_Exitosa")

        # Paso 2: Validación en DB (Alta)
        logger.info("Paso 2: Validando persistencia en Base de Datos (Post-Alta)")
        registro_db = repo_db.obtener_registro(valor)

        capturar_evidencia_sql(nombre_caso, "02_SQL_Alta", query_sql, [valor], registro_db)

        if not registro_db:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Alta_No_Persistida_DB",
                                         f"El registro '{valor}' no fue encontrado en la DB tras la alta en UI.")

        # Paso 3: Eliminación del registro vía UI
        logger.info("Paso 3: Localizando y eliminando el registro creado")

        if not self.ui.buscar_en_paginacion(valor):
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Registro_No_Visible_UI",
                                         f"El registro '{valor}' no está visible en la grilla para proceder con la baja.")

        self.ui.seleccionar_registro_en_grid(valor)

        if not self.ui.es_boton_eliminar_habilitado():
            BugReporter.certificar_falla(
                self.page, logger, nombre_caso, "Boton_Eliminar_Blocked",
                "El botón 'Eliminar' quedó bloqueado para el registro recién creado.")

        self.ui.click_eliminar()
        self.ui.click_guardar()
        self.ui.esperar_alerta_exito()

        if self.ui.buscar_en_paginacion(valor):
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Registro_No_Eliminado",
                                         f"El registro '{valor}' está visible en la grilla despues proceder con la baja.")

        capturar_evidencia(self.page, nombre_caso, "03_UI_Baja_Exitosa")

        # Paso 4: Validación en DB (Baja)
        logger.info("Paso 4: Validando eliminación real en la Base de Datos")
        eliminado = repo_db.esperar_no_existencia(valor)

        registro_final = repo_db.obtener_registro(valor)

        capturar_evidencia_sql(nombre_caso=nombre_caso, nombre_paso="04_SQL_Baja_Verificacion", query=query_sql,
                               params=[valor], resultado=registro_final)

        if not eliminado:
            BugReporter.certificar_falla(self.page, logger, nombre_caso, "Baja_No_Persistida_DB",
                                         f"El registro '{valor}' todavía existe en la base de datos tras la eliminación en UI.")

        logger.info(f"=== FIN FLUJO E2E: CICLO COMPLETO EXITOSO [{valor}] ===")
        return True
