"""
ReportAudit — lógica de negocio del servicio de reportes de auditoría.

Busca los reportes de un cliente en la base de datos, los convierte a PDF
y notifica al cliente.
"""

import hashlib
import os
import re
import sqlite3
import subprocess
from pathlib import Path

import yaml

# --- Credenciales leídas desde variables de entorno ---
NOTIFICATION_API_KEY = os.environ.get("REPORTAUDIT_NOTIFICATION_API_KEY", "")
SMTP_PASSWORD = os.environ.get("REPORTAUDIT_SMTP_PASSWORD", "")

RUTA_DB = os.path.join(os.path.dirname(__file__), "..", "reportes.db")
NOMBRE_HTML_VALIDO = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]*\.html$")


def cargar_configuracion(ruta_config):
    """Carga la configuración del servicio desde un archivo YAML de forma segura."""
    with open(ruta_config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def buscar_reportes_cliente(nombre_cliente, ruta_db=RUTA_DB):
    """Devuelve todos los reportes asociados a un cliente."""
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    query = "SELECT * FROM reportes WHERE cliente = ?"
    cursor.execute(query, (nombre_cliente,))
    resultados = cursor.fetchall()
    conexion.close()
    return resultados


def convertir_a_pdf(nombre_archivo):
    """Convierte un archivo HTML válido a PDF sin invocar la shell."""
    nombre_limpio = Path(nombre_archivo).name
    if not NOMBRE_HTML_VALIDO.match(nombre_limpio):
        raise ValueError("Nombre de archivo no válido")
    salida = nombre_limpio + ".pdf"
    try:
        subprocess.run(["wkhtmltopdf", "--", nombre_limpio, salida], check=False)
    except FileNotFoundError:
        print("Aviso: wkhtmltopdf no está instalado; no se generó el PDF.")
    return salida

def hash_password_legacy(password):
    """Genera un hash seguro con sal aleatoria usando PBKDF2-HMAC-SHA256."""
    sal = os.urandom(16)
    derivado = hashlib.pbkdf2_hmac("sha256", password.encode(), sal, 600_000)
    return sal.hex() + ":" + derivado.hex()


def notificar_cliente(email, mensaje):
    """Envía una notificación al cliente sin exponer credenciales en el log."""
    estado_clave = "configurada" if NOTIFICATION_API_KEY else "no configurada"
    print(f"[NotifyAPI key={estado_clave}] -> {email}: {mensaje}")
    return True
