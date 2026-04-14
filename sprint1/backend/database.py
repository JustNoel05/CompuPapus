# ─────────────────────────────────────────────────────────────────────────────
# database.py — BetDecision / CompuPapus
# Sprint 1 — Conexión MySQL + Autenticación de usuarios
# Nota: Tablas de sugerencias e historial se agregan en Sprint 3-4
# ─────────────────────────────────────────────────────────────────────────────

import mysql.connector
from mysql.connector import Error


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN — ajustar según entorno local (Laragon / XAMPP)
# ─────────────────────────────────────────────────────────────────────────────

CONFIG_SIN_DB = {
    "host":     "localhost",
    "user":     "root",
    "password": "",           # ← cambiar por contraseña local de MySQL
}

CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",           # ← cambiar por contraseña local de MySQL
    "database": "betdecision"
}


# ─────────────────────────────────────────────────────────────────────────────
# CONEXIÓN
# ─────────────────────────────────────────────────────────────────────────────

def conectar():
    try:
        conn = mysql.connector.connect(**CONFIG)
        return conn
    except Error as e:
        print(f"[ERROR] No se pudo conectar a MySQL: {e}")
        return None


def crear_base_datos():
    try:
        conn = mysql.connector.connect(**CONFIG_SIN_DB)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS betdecision")
        conn.commit()
        cursor.close()
        conn.close()
        print("[OK] Base de datos betdecision verificada.")
    except Error as e:
        print(f"[ERROR] No se pudo crear la base de datos: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN — Sprint 1 solo crea la tabla usuarios
# ─────────────────────────────────────────────────────────────────────────────

def inicializar_db():
    """
    Sprint 1: crea únicamente la tabla usuarios.
    Las tablas sugerencias y detalle_sugerencia se añaden en Sprint 3.
    """
    crear_base_datos()
    conn = conectar()
    if not conn:
        return

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            nombre     VARCHAR(100) NOT NULL,
            correo     VARCHAR(150) NOT NULL UNIQUE,
            password   VARCHAR(255) NOT NULL,
            creado_en  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("[OK] Tabla usuarios verificada (Sprint 1).")


# ─────────────────────────────────────────────────────────────────────────────
# USUARIOS — Historia H1
# ─────────────────────────────────────────────────────────────────────────────

def registrar_usuario(nombre, correo, password):
    """
    Registra un nuevo usuario.
    Retorna {"ok": True, "id": id} o {"ok": False, "error": mensaje}
    """
    conn = conectar()
    if not conn:
        return {"ok": False, "error": "Sin conexión a la base de datos"}

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, password) VALUES (%s, %s, %s)",
            (nombre, correo, password)
        )
        conn.commit()
        return {"ok": True, "id": cursor.lastrowid}

    except mysql.connector.IntegrityError:
        return {"ok": False, "error": "El correo ya está registrado"}

    except Error as e:
        return {"ok": False, "error": str(e)}

    finally:
        cursor.close()
        conn.close()


def login_usuario(correo, password):
    """
    Valida las credenciales del usuario.
    Retorna {"ok": True, "id": id, "nombre": nombre} o {"ok": False, "error": mensaje}
    """
    conn = conectar()
    if not conn:
        return {"ok": False, "error": "Sin conexión a la base de datos"}

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nombre FROM usuarios WHERE correo=%s AND password=%s",
            (correo, password)
        )
        usuario = cursor.fetchone()

        if usuario:
            return {"ok": True, "id": usuario["id"], "nombre": usuario["nombre"]}
        else:
            return {"ok": False, "error": "Correo o contraseña incorrectos"}

    except Error as e:
        return {"ok": False, "error": str(e)}

    finally:
        cursor.close()
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# Prueba — ejecutar para verificar conexión y registro
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Sprint 1 — Inicializando base de datos...")
    inicializar_db()

    print("\n→ Probando registro...")
    r = registrar_usuario("Axel Gómez", "axel@compupapus.com", "123456")
    print(f"  Registro: {r}")

    print("\n→ Probando login correcto...")
    s = login_usuario("axel@compupapus.com", "123456")
    print(f"  Login: {s}")

    print("\n→ Probando login incorrecto...")
    s2 = login_usuario("axel@compupapus.com", "wrongpass")
    print(f"  Login fallido: {s2}")
