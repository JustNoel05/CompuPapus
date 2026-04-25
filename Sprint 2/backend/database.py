# ─────────────────────────────────────────────────────────────────────────────
# database.py — CompuPapus / BetDecision
# Conexión y consultas a MySQL
# Gestiona: usuarios, sesiones, sugerencias e historial
# ─────────────────────────────────────────────────────────────────────────────

import mysql.connector
from mysql.connector import Error


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE CONEXIÓN
# Cambiar los valores según el entorno local de cada integrante
# ─────────────────────────────────────────────────────────────────────────────

# Conexión sin base de datos — solo para crearla si no existe
CONFIG_SIN_DB = {
    "host":     "localhost",
    "user":     "root",
    "password": "",           # ← cambiar por tu contraseña de MySQL
}

# Conexión normal con base de datos
CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",           # ← cambiar por tu contraseña de MySQL
    "database": "BetDecision"
}


# ─────────────────────────────────────────────────────────────────────────────
# CONEXIÓN
# ─────────────────────────────────────────────────────────────────────────────

def conectar():
    """
    Abre y retorna una conexión a MySQL.
    Si falla, imprime el error y retorna None.
    """
    try:
        conn = mysql.connector.connect(**CONFIG)
        return conn
    except Error as e:
        print(f"[ERROR] No se pudo conectar a MySQL: {e}")
        return None


def crear_base_datos():
    """
    Crea la base de datos sora_mx si no existe.
    Se ejecuta antes de inicializar_db() para evitar
    el error 'Unknown database'.
    """
    try:
        conn = mysql.connector.connect(**CONFIG_SIN_DB)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS sora_mx")
        conn.commit()
        cursor.close()
        conn.close()
        print("[OK] Base de datos sora_mx verificada.")
    except Error as e:
        print(f"[ERROR] No se pudo crear la base de datos: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN — crear tablas si no existen
# ─────────────────────────────────────────────────────────────────────────────

def inicializar_db():
    """
    Crea la base de datos y las tablas necesarias si no existen.
    Se llama automáticamente al arrancar FastAPI.

    Tablas:
        usuarios          → datos de acceso
        sugerencias       → cabecera de cada recomendación
        detalle_sugerencia→ partidos individuales de cada sugerencia
    """
    crear_base_datos()   # crea sora_mx si no existe
    conn = conectar()
    if not conn:
        return

    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            nombre     VARCHAR(100) NOT NULL,
            correo     VARCHAR(150) NOT NULL UNIQUE,
            password   VARCHAR(255) NOT NULL,
            creado_en  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla de sugerencias (cabecera)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sugerencias (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id    INT NOT NULL,
            jornada       VARCHAR(50) NOT NULL,
            capital       DECIMAL(10,2) NOT NULL,
            ganancia_est  DECIMAL(10,2) NOT NULL,
            fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    # Tabla de detalle por partido
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_sugerencia (
            id              INT AUTO_INCREMENT PRIMARY KEY,
            sugerencia_id   INT NOT NULL,
            partido         VARCHAR(100) NOT NULL,
            resultado_sug   VARCHAR(20) NOT NULL,
            momio           DECIMAL(6,2) NOT NULL,
            probabilidad    DECIMAL(5,1) NOT NULL,
            apuesta         DECIMAL(10,2) NOT NULL,
            acerto          TINYINT DEFAULT NULL,   -- NULL=pendiente 1=sí 0=no
            FOREIGN KEY (sugerencia_id) REFERENCES sugerencias(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("[OK] Base de datos inicializada correctamente.")


# ─────────────────────────────────────────────────────────────────────────────
# USUARIOS
# ─────────────────────────────────────────────────────────────────────────────

def registrar_usuario(nombre, correo, password):
    """
    Registra un nuevo usuario en la base de datos.

    Retorna:
        {"ok": True, "id": usuario_id}  si se registró correctamente
        {"ok": False, "error": mensaje} si el correo ya existe u otro error
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

    Retorna:
        {"ok": True,  "id": id, "nombre": nombre} si son correctas
        {"ok": False, "error": mensaje}            si son incorrectas
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
# SUGERENCIAS
# ─────────────────────────────────────────────────────────────────────────────

def guardar_sugerencia(usuario_id, jornada, capital, ganancia_est, partidos):
    """
    Guarda una sugerencia completa con su detalle por partido.

    Parámetros:
        usuario_id   → id del usuario autenticado
        jornada      → nombre de la jornada (ej: "Jornada 11")
        capital      → capital ingresado por el usuario
        ganancia_est → ganancia estimada total
        partidos     → lista de dicts con:
                       partido, resultado_sug, momio, probabilidad, apuesta

    Retorna:
        {"ok": True,  "id": sugerencia_id}
        {"ok": False, "error": mensaje}
    """
    conn = conectar()
    if not conn:
        return {"ok": False, "error": "Sin conexión a la base de datos"}

    try:
        cursor = conn.cursor()

        # Insertar cabecera de la sugerencia
        cursor.execute(
            """INSERT INTO sugerencias
               (usuario_id, jornada, capital, ganancia_est)
               VALUES (%s, %s, %s, %s)""",
            (usuario_id, jornada, capital, ganancia_est)
        )
        sugerencia_id = cursor.lastrowid

        # Insertar cada partido del detalle
        for p in partidos:
            cursor.execute(
                """INSERT INTO detalle_sugerencia
                   (sugerencia_id, partido, resultado_sug, momio, probabilidad, apuesta)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    sugerencia_id,
                    p["partido"],
                    p["resultado"],
                    p["momio"],
                    p["prob"],
                    p["peso"],
                )
            )

        conn.commit()
        return {"ok": True, "id": sugerencia_id}

    except Error as e:
        conn.rollback()
        return {"ok": False, "error": str(e)}

    finally:
        cursor.close()
        conn.close()


def get_historial(usuario_id):
    """
    Obtiene el historial completo de sugerencias de un usuario,
    incluyendo el detalle de cada partido.

    Retorna lista de sugerencias ordenadas de más reciente a más antigua.
    Cada sugerencia incluye su lista de partidos con estado de acierto.
    """
    conn = conectar()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)

        # Obtener cabeceras de sugerencias
        cursor.execute(
            """SELECT id, jornada, capital, ganancia_est, fecha
               FROM sugerencias
               WHERE usuario_id = %s
               ORDER BY fecha DESC""",
            (usuario_id,)
        )
        sugerencias = cursor.fetchall()

        # Para cada sugerencia, obtener el detalle de partidos
        for sug in sugerencias:
            cursor.execute(
                """SELECT id, partido, resultado_sug, momio,
                          probabilidad, apuesta, acerto
                   FROM detalle_sugerencia
                   WHERE sugerencia_id = %s""",
                (sug["id"],)
            )
            sug["partidos"] = cursor.fetchall()

            # Calcular % de aciertos de esta sugerencia
            partidos_marcados = [
                p for p in sug["partidos"] if p["acerto"] is not None]
            if partidos_marcados:
                aciertos = sum(
                    1 for p in partidos_marcados if p["acerto"] == 1)
                sug["pct_aciertos"] = round(
                    aciertos / len(partidos_marcados) * 100, 1)
            else:
                sug["pct_aciertos"] = None   # aún sin marcar

        return sugerencias

    except Error as e:
        print(f"[ERROR] get_historial: {e}")
        return []

    finally:
        cursor.close()
        conn.close()


def marcar_acierto(detalle_id, acerto):
    """
    Marca si un partido de una sugerencia acertó o no.

    Parámetros:
        detalle_id → id del registro en detalle_sugerencia
        acerto     → True (acertó) / False (falló)

    Retorna:
        {"ok": True}  o  {"ok": False, "error": mensaje}
    """
    conn = conectar()
    if not conn:
        return {"ok": False, "error": "Sin conexión a la base de datos"}

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE detalle_sugerencia SET acerto = %s WHERE id = %s",
            (1 if acerto else 0, detalle_id)
        )
        conn.commit()
        return {"ok": True}

    except Error as e:
        return {"ok": False, "error": str(e)}

    finally:
        cursor.close()
        conn.close()


def get_pct_aciertos_global(usuario_id):
    """
    Calcula el porcentaje de aciertos acumulado del usuario
    sobre todos los partidos que ha marcado.

    Retorna float entre 0 y 100, o None si no hay partidos marcados.
    """
    conn = conectar()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT
                 COUNT(*)                            AS total,
                 SUM(CASE WHEN acerto=1 THEN 1 END)  AS aciertos
               FROM detalle_sugerencia ds
               JOIN sugerencias s ON ds.sugerencia_id = s.id
               WHERE s.usuario_id = %s
                 AND ds.acerto IS NOT NULL""",
            (usuario_id,)
        )
        row = cursor.fetchone()
        total, aciertos = row

        if not total:
            return None

        return round((aciertos / total) * 100, 1)

    except Error as e:
        print(f"[ERROR] get_pct_aciertos_global: {e}")
        return None

    finally:
        cursor.close()
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# PRUEBA — correr directamente para verificar conexión
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Inicializando base de datos...")
    inicializar_db()

    print("\nProbando registro de usuario...")
    resultado = registrar_usuario("Axel Gómez", "axel@compupapus.com", "1234")
    print(f"  Registro: {resultado}")

    print("\nProbando login...")
    sesion = login_usuario("axel@compupapus.com", "1234")
    print(f"  Login: {sesion}")

    if sesion["ok"]:
        print("\nProbando guardar sugerencia...")
        r = guardar_sugerencia(
            usuario_id=sesion["id"],
            jornada="Jornada 11",
            capital=500,
            ganancia_est=69.72,
            partidos=[
                {"partido": "Puebla vs Necaxa",       "resultado": "Visitante",
                 "momio": 1.35, "prob": 74.2, "peso": 83},
                {"partido": "Toluca vs Atlas",         "resultado": "Local",
                 "momio": 1.30, "prob": 77.1, "peso": 83},
                {"partido": "Tigres vs Querétaro",     "resultado": "Local",
                 "momio": 1.32, "prob": 75.8, "peso": 83},
            ]
        )
        print(f"  Sugerencia guardada: {r}")

        print("\nProbando historial...")
        historial = get_historial(sesion["id"])
        print(f"  Sugerencias encontradas: {len(historial)}")
        for sug in historial:
            print(f"  → {sug['jornada']} | Capital: ${sug['capital']} | "
                  f"Partidos: {len(sug['partidos'])}")
