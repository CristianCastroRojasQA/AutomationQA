import sys
import os

# Añadimos la raíz del proyecto al path para que encuentre los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_manager import db_manager
from config.settings import settings


def test_manual_db_connection():
    print("\n" + "=" * 50)
    print("🧪 INICIANDO PRUEBA DE CONEXIÓN DINÁMICA")
    print("=" * 50)

    # 1. Validar qué datos leyó Settings
    print(f"📌 Proyecto Detectado: {settings.PROYECTO}")
    print(f"📌 Ambiente Detectado: {settings.AMBIENTE}")
    print(f"📌 Base de Datos a conectar: {settings.DB_NAME}")
    print(f"📌 Servidor: {settings.DB_SERVER}")
    print(f"📌 Usuario: {settings.DB_USER}")
    print("-" * 50)

    # 2. Ejecutar la validación del Manager
    resultado = db_manager.validar_conexion()

    if resultado:
        print("\n✅ PRUEBA EXITOSA: La base de datos está alcanzable y responde.")
    else:
        print("\n❌ PRUEBA FALLIDA: Revisa las credenciales, la VPN o el Driver de SQL Server.")

    print("=" * 50 + "\n")


if __name__ == "__main__":
    test_manual_db_connection()
