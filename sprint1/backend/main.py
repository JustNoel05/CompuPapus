# ─────────────────────────────────────────────────────────────────────────────
# main.py — BetDecision / CompuPapus
# Sprint 1 — FastAPI base
# Rutas implementadas este sprint: /registro, /login, /partidos
# Rutas pendientes (Sprint 2-4): /calcular, /guardar, /historial, /acierto
# ─────────────────────────────────────────────────────────────────────────────
# Iniciar: uvicorn main:app --reload
# Docs:    http://localhost:8000/docs
# ─────────────────────────────────────────────────────────────────────────────

from contextlib import asynccontextmanager  # lifespan moderno (Python 3.10+)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import os

import regresion
import database


# ─────────────────────────────────────────────────────────────────────────────
# RUTAS DE ARCHIVOS
# Se calculan una sola vez al importar el módulo
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')
# Sprint 1: los HTML viven directamente en frontend/, sin subcarpeta templates/
TEMPLATES_DIR = FRONTEND_DIR


# ─────────────────────────────────────────────────────────────────────────────
# LIFESPAN — reemplaza el on_event("startup") deprecado
# ─────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que corre al INICIAR el servidor
    database.inicializar_db()
    print("[OK] BetDecision Sprint 1 — servidor iniciado.")
    yield
    # Código que correría al APAGAR (vacío por ahora)


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="BetDecision — Sprint 1",
    description="CompuPapus | Análisis de Algoritmos | UdG CUCEI 2026",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos solo si la carpeta ya existe
# (en Sprint 1 puede no existir todavía)
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    print(f"[OK] Carpeta static montada: {STATIC_DIR}")
else:
    print(f"[AVISO] Carpeta static no encontrada ({STATIC_DIR}). "
          "Las páginas HTML se sirven directamente sin CSS externo.")


def _html(nombre_archivo: str):
    """Sirve un archivo HTML desde la carpeta frontend/."""
    ruta = os.path.join(TEMPLATES_DIR, nombre_archivo)
    if os.path.isfile(ruta):
        return FileResponse(ruta)
    return HTMLResponse(
        f"<h3>Archivo no encontrado: {nombre_archivo}</h3>"
        "<p>Asegúrate de que el HTML esté en la carpeta <code>frontend/</code>.</p>",
        status_code=404
    )


@app.get("/")
def root():
    return _html('login.html')


@app.get("/login")
def page_login():
    return _html('login.html')


@app.get("/partidos-page")
def page_partidos():
    return _html('pantalla1.html')

# Rutas de pantalla 2 y 3 — pendientes Sprint 2 y 4
# @app.get("/optimizar-page") → Sprint 2
# @app.get("/historial-page") → Sprint 4


# ─────────────────────────────────────────────────────────────────────────────
# MODELOS Pydantic
# ─────────────────────────────────────────────────────────────────────────────

class RegistroRequest(BaseModel):
    nombre:   str
    correo:   str
    password: str


class LoginRequest(BaseModel):
    correo:   str
    password: str


# ─────────────────────────────────────────────────────────────────────────────
# RUTA 1 — REGISTRO  (H1)
# POST /registro
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/registro")
def registro(data: RegistroRequest):
    """
    Historia H1 — Registro de usuario.
    Almacena nombre, correo y contraseña en MySQL.
    """
    resultado = database.registrar_usuario(
        data.nombre, data.correo, data.password)
    if not resultado["ok"]:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return {"ok": True, "id": resultado["id"], "mensaje": "Usuario registrado correctamente"}


# ─────────────────────────────────────────────────────────────────────────────
# RUTA 2 — LOGIN  (H1)
# POST /login
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/login")
def login(data: LoginRequest):
    """
    Historia H1 — Login de usuario.
    Valida credenciales contra MySQL.
    """
    resultado = database.login_usuario(data.correo, data.password)
    if not resultado["ok"]:
        raise HTTPException(status_code=401, detail=resultado["error"])
    return {"ok": True, "id": resultado["id"], "nombre": resultado["nombre"]}


# ─────────────────────────────────────────────────────────────────────────────
# RUTA 3 — PARTIDOS  (H2 inicio)
# GET /partidos
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/partidos")
def get_partidos():
    """
    Historia H2 — Inicio.
    Devuelve los partidos de la jornada con momios objetivos y EV calculados
    por regresión lineal, ordenados de mayor a menor EV recomendado.
    """
    try:
        partidos = regresion.calcular_momios()
        return {
            "ok":       True,
            "jornada":  "Jornada 15",
            "total":    len(partidos),
            "partidos": partidos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# RUTAS PENDIENTES — se implementan en sprints posteriores
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/calcular")
def calcular():
    """Sprint 2 — Comparativa de algoritmos Knapsack."""
    raise HTTPException(status_code=501, detail="Pendiente — Sprint 2")


@app.post("/guardar")
def guardar():
    """Sprint 3 — Guardar sugerencia en MySQL."""
    raise HTTPException(status_code=501, detail="Pendiente — Sprint 3")


@app.get("/historial/{usuario_id}")
def historial(usuario_id: int):
    """Sprint 4 — Historial del usuario."""
    raise HTTPException(status_code=501, detail="Pendiente — Sprint 4")


@app.post("/acierto")
def acierto():
    """Sprint 4 — Marcar acierto/fallo."""
    raise HTTPException(status_code=501, detail="Pendiente — Sprint 4")


# ─────────────────────────────────────────────────────────────────────────────
# ARRANCAR
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
