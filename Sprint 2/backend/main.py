# ─────────────────────────────────────────────────────────────────────────────
# main.py — CompuPapus / BetDecision
# Backend FastAPI — puente entre el frontend HTML/JS y Python
# Rutas: login, partidos, calcular, guardar, historial, acierto
# ─────────────────────────────────────────────────────────────────────────────

# Iniciar: uvicorn main:app --reload

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

import regresion
import algoritmos
import database


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="BetDecision",
    description="CompuPapus | Análisis de Algoritmos | UdG CUCEI 2026",
    version="1.0.0"
)

# Permitir que el frontend HTML/JS pueda hacer fetch() al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # en producción cambiar por el dominio real
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar base de datos al arrancar


@app.on_event("startup")
def startup():
    database.inicializar_db()
    print("[OK] BetDecision backend iniciado.")


# ─────────────────────────────────────────────────────────────────────────────
# MODELOS — estructura de los datos que llegan del frontend (JSON)
# ─────────────────────────────────────────────────────────────────────────────

class RegistroRequest(BaseModel):
    nombre:   str
    correo:   str
    password: str


class LoginRequest(BaseModel):
    correo:   str
    password: str


class CalcularRequest(BaseModel):
    capital: float


class PartidoDetalle(BaseModel):
    partido:    str
    resultado:  str
    momio:      float
    prob:       float
    peso:       float


class GuardarRequest(BaseModel):
    usuario_id:   int
    jornada:      str
    capital:      float
    ganancia_est: float
    partidos:     List[PartidoDetalle]


class AciertoRequest(BaseModel):
    detalle_id: int
    acerto:     bool


# ─────────────────────────────────────────────────────────────────────────────
# ARCHIVOS ESTÁTICOS — sirve el frontend desde FastAPI
# Estructura esperada:
#   SORA_Mx/
#   ├── backend/    ← main.py está aquí
#   └── frontend/
#       ├── templates/
#       └── static/
# ─────────────────────────────────────────────────────────────────────────────

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, 'templates')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')

# Servir archivos estáticos (CSS, JS)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Ruta raíz → redirige a login.html


@app.get("/")
def root():
    return FileResponse(os.path.join(TEMPLATES_DIR, 'login.html'))

# Rutas para cada pantalla HTML


@app.get("/login")
def page_login():
    return FileResponse(os.path.join(TEMPLATES_DIR, 'login.html'))


@app.get("/partidos-page")
def page_partidos():
    return FileResponse(os.path.join(TEMPLATES_DIR, 'pantalla1.html'))


@app.get("/optimizar-page")
def page_optimizar():
    return FileResponse(os.path.join(TEMPLATES_DIR, 'pantalla2.html'))


@app.get("/historial-page")
def page_historial():
    return FileResponse(os.path.join(TEMPLATES_DIR, 'pantalla3.html'))


# ─────────────────────────────────────────────────────────────────────────────
# RUTA 1 — REGISTRO DE USUARIO
# POST /registro
# Recibe: nombre, correo, password
# Retorna: ok, id del nuevo usuario
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/registro")
def registro(data: RegistroRequest):
    """
    Registra un nuevo usuario en MySQL.
    Si el correo ya existe retorna error 400.
    """
    resultado = database.registrar_usuario(
        data.nombre,
        data.correo,
        data.password
    )
    if not resultado["ok"]:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return {"ok": True, "id": resultado["id"], "mensaje": "Usuario registrado correctamente"}


# ─────────────────────────────────────────────────────────────────────────────
# RUTA 2 — LOGIN
# POST /login
# Recibe: correo, password
# Retorna: ok, id, nombre del usuario
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/login")
def login(data: LoginRequest):
    """
    Valida las credenciales del usuario.
    Si son incorrectas retorna error 401.
    """
    resultado = database.login_usuario(data.correo, data.password)
    if not resultado["ok"]:
        raise HTTPException(status_code=401, detail=resultado["error"])
    return {
        "ok":     True,
        "id":     resultado["id"],
        "nombre": resultado["nombre"]
    }


# ─────────────────────────────────────────────────────────────────────────────
# RUTA 3 — PARTIDOS DE LA JORNADA (Pantalla 1)
# GET /partidos
# Retorna: lista de partidos ordenados por EV descendente
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/partidos")
def get_partidos():
    """
    Calcula los momios objetivos de la jornada usando regresión lineal
    y devuelve los partidos ordenados de mayor a menor EV.
    Los partidos con EV positivo son los candidatos al Knapsack.
    """
    try:
        partidos = regresion.calcular_momios()
        return {
            "ok":       True,
            "total":    len(partidos),
            "partidos": partidos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# RUTA 4 — CALCULAR DISTRIBUCIÓN ÓPTIMA (Pantalla 2)
# POST /calcular
# Recibe: capital del usuario
# Retorna: resultados de los 3 algoritmos + algoritmo ganador
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/calcular")
def calcular(data: CalcularRequest):
    """
    Filtra los partidos con EV positivo y corre los 3 algoritmos Knapsack.
    Retorna la distribución óptima del capital y la comparativa de algoritmos.
    """
    if data.capital <= 0:
        raise HTTPException(
            status_code=400, detail="El capital debe ser mayor a 0")

    try:
        # Obtener partidos con EV positivo
        todos = regresion.calcular_momios()
        positivos = [p for p in todos if p["ev_positivo"]]

        if not positivos:
            raise HTTPException(
                status_code=404,
                detail="No hay partidos con EV positivo en esta jornada"
            )

        # Correr los 3 algoritmos
        resultado = algoritmos.comparar(positivos, data.capital)

        # Obtener la selección del algoritmo ganador (Programación Dinámica)
        pd = resultado["programacion_dinamica"]

        return {
            "ok":               True,
            "capital":          data.capital,
            "partidos_disponibles": len(positivos),
            "distribucion":     pd["seleccion"],
            "total_apostado":   pd["total_apostado"],
            "ganancia_estimada": pd["ganancia_estimada"],
            "algoritmo_usado":  pd["algoritmo"],
            # Comparativa para el reporte académico (no se muestra al usuario)
            "comparativa": {
                "fuerza_bruta": {
                    "ganancia":      resultado["fuerza_bruta"]["ganancia_estimada"],
                    "tiempo_ms":     resultado["fuerza_bruta"]["tiempo_ms"],
                    "complejidad":   resultado["fuerza_bruta"]["complejidad"],
                },
                "programacion_dinamica": {
                    "ganancia":      pd["ganancia_estimada"],
                    "tiempo_ms":     pd["tiempo_ms"],
                    "complejidad":   pd["complejidad"],
                },

                "ganador": resultado["ganador"]
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# RUTA 5 — GUARDAR SUGERENCIA
# POST /guardar
# Recibe: usuario_id, jornada, capital, ganancia_est, lista de partidos
# Retorna: ok, id de la sugerencia guardada
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/guardar")
def guardar(data: GuardarRequest):
    """
    Guarda la sugerencia del usuario en MySQL con el detalle de cada partido.
    """
    partidos = [p.dict() for p in data.partidos]
    resultado = database.guardar_sugerencia(
        usuario_id=data.usuario_id,
        jornada=data.jornada,
        capital=data.capital,
        ganancia_est=data.ganancia_est,
        partidos=partidos
    )
    if not resultado["ok"]:
        raise HTTPException(status_code=500, detail=resultado["error"])
    return {
        "ok":  True,
        "id":  resultado["id"],
        "mensaje": "Sugerencia guardada correctamente"
    }


# ─────────────────────────────────────────────────────────────────────────────
# RUTA 6 — HISTORIAL DEL USUARIO (Pantalla 3)
# GET /historial/{usuario_id}
# Retorna: lista de sugerencias con detalle y % de aciertos
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/historial/{usuario_id}")
def historial(usuario_id: int):
    """
    Devuelve el historial completo de sugerencias del usuario
    con el detalle de cada partido y su estado de acierto.
    """
    data = database.get_historial(usuario_id)
    pct = database.get_pct_aciertos_global(usuario_id)

    return {
        "ok":             True,
        "usuario_id":     usuario_id,
        "pct_aciertos":   pct,
        "total_jornadas": len(data),
        "historial":      data
    }


# ─────────────────────────────────────────────────────────────────────────────
# RUTA 7 — MARCAR ACIERTO (Pantalla 3)
# POST /acierto
# Recibe: detalle_id, acerto (true/false)
# Retorna: ok
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/acierto")
def acierto(data: AciertoRequest):
    """
    Marca si el sistema acertó o no en un partido específico.
    El usuario presiona ✓ o ✗ en Pantalla 3.
    """
    resultado = database.marcar_acierto(data.detalle_id, data.acerto)
    if not resultado["ok"]:
        raise HTTPException(status_code=500, detail=resultado["error"])
    return {"ok": True, "mensaje": "Acierto registrado correctamente"}


# ─────────────────────────────────────────────────────────────────────────────
# ARRANCAR EL SERVIDOR
# Ejecutar: uvicorn main:app --reload
# Docs:     http://localhost:8000/docs
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
