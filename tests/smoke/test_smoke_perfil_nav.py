import pytest

from pages.common.perfil_page import PerfilPage
from utils.common_actions import realizar_login_obligatorio, finalizar_sesion_segura
from utils.logger import get_logger
from utils.test_orchestrator import TestOrchestrator


@pytest.mark.smoke
@pytest.mark.perfil
def test_smoke_opciones_perfil(auth, page):
    nombre_caso_prueba = "Smoke_Opciones_Perfil"
    logger= get_logger(nombre_caso_prueba)
    perfil = PerfilPage(page)

    realizar_login_obligatorio(auth, nombre_caso_prueba, logger)

    rutas_perfil = [
        ("Perfil > Fecha de Negocio", perfil.validar_fecha_negocio_modal),
        ("Perfil > Cambiar Contraseña", perfil.navegar_a_cambiar_contrasena),
        ("Perfil > Acerca de", perfil.validar_version_ambiente)
    ]

    engine = TestOrchestrator(page, logger, nombre_caso_prueba)
    try:
        engine.ejecutar_flujo(rutas_perfil)
    finally:
        finalizar_sesion_segura(auth, logger, nombre_caso_prueba)
