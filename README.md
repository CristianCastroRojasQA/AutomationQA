# 🤖 AutomationQA

Framework de automatización de pruebas UI con **Playwright** y **Pytest** para GETNET.

## ⚡ Inicio Rápido

### 1. Activar entorno virtual

```powershell
.\venv\Scripts\activate
```

### 2. Configurar `.env`

```bash
cp .env.example .env
```

Edita `.env` con URL, usuario y contraseña de tu ambiente.

### 3. Ejecutar tests

```bash
pytest tests/ -v
```

Los reportes se generan automáticamente en `reports/report.html`.

## 📂 Estructura

```bash
config/          # Configuración centralizada desde .env
flows/           # Flujos de negocio (login, logout)
pages/           # Page Objects con selectores y acciones
tests/           # Casos de prueba
utils/           # Logging y captura de evidencias
logs/            # Archivo de logs (generado automáticamente)
screenshots/     # Evidencias de pruebas (generadas automáticamente)
reports/         # Reportes HTML (generados automáticamente)
```

## 🧪 Test Actual

El proyecto contiene **un test de smoke** que valida el flujo completo:

```python
def test_login_home_logout_env(page):
    """Login → Validar home → Logout"""
    auth.login_con_env()
    auth.logout()
```

## ⚙️ Configuración Disponible

| Variable | Valor | Propósito |
| -------- | ----- | --------- |
| AMBIENTE | QA, CERT, PROD | Ambiente de ejecución |
| BROWSER | chromium, firefox, webkit | Navegador a usar |
| HEADLESS | true/false | Navegador visible o no |
| SCREENSHOT_ON_FAIL | true/false | Capturar screenshots en fallos |

## 📊 Características

✅ **Reportes HTML** automáticos  
✅ **Screenshots** capturados en fallos  
✅ **Logs duales** (consola + archivo rotativo)  
✅ **Page Object Model** para mantenibilidad  
✅ **Configuración por variables de entorno**

## 📝 Ejecutar un Test Específico

```bash
pytest tests/test_smoke_framework.py::test_login_home_logout_env -v
```

## 🔍 Ver Logs

```bash
pytest -s  # Logs en tiempo real
tail -f logs/ejecucion.log  # Archivo de logs
```

## 📦 Dependencias

- Python 3.8+
- Playwright 1.40+
- Pytest 9.0+
