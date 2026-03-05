from flows.auth_flow import AuthFlow
from utils.logger import get_logger


def test_TC_000001_login_exitoso(page, request):
    caso = getattr(
        request.node, "originalname", request.node.name
    )
    log = get_logger(caso)

    log.info(f"INICIO - {caso}")

    auth = AuthFlow(page)
    auth.login_con_env(caso=caso)
    auth.logout(caso=caso)

    log.info(f"FIN - {caso}")
