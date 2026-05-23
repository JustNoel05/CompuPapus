# ─────────────────────────────────────────────────────────────────────────────
# main.py — CompuPapus / BetDesicion
# Backend FastAPI — puente entre el frontend HTML/JS y Python
# Rutas: login, partidos, calcular, guardar, historial, acierto
# ─────────────────────────────────────────────────────────────────────────────

# Iniciar: uvicorn main:app --reload

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel
from typing import List, Optional

import regresion
import algoritmos
import database
import huffman


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="BetDesicion — Sistema de Optimización y Recomendación de Apuestas",
    description="CompuPapus | Análisis de Algoritmos | UdG CUCEI 2026",
    version="1.0.0"
)

# Permitir que el frontend HTML/JS pueda hacer fetch() al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar base de datos al arrancar


@app.on_event("startup")
def startup():
    database.inicializar_db()
    print("[OK] BetDesicion backend iniciado.")


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
#   BetDesicion/
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
                "greedy": {
                    "ganancia":      resultado["greedy"]["ganancia_estimada"],
                    "tiempo_ms":     resultado["greedy"]["tiempo_ms"],
                    "complejidad":   resultado["greedy"]["complejidad"],
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
# RUTA 8 — DESCARGAR HISTORIAL COMPRIMIDO CON HUFFMAN (Pantalla 3)
# GET /descargar-historial/{usuario_id}
# Genera el reporte en texto plano, lo comprime con Huffman y lo descarga
# Complejidad del algoritmo: O(n log n) donde n = símbolos únicos del reporte
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/descargar-historial/{usuario_id}")
def descargar_historial(usuario_id: int):
    """
    Genera el reporte de historial del usuario, aplica compresión
    Huffman y devuelve el archivo como descarga en texto plano.

    El archivo incluye:
      - Contenido legible del historial (partidos, montos, aciertos)
      - Métricas de compresión Huffman (tasa, bits, tabla de códigos)
      - Complejidad algorítmica documentada

    El texto crece con cada jornada guardada, haciendo la compresión
    cada vez más significativa — justificación académica del algoritmo.
    """
    # Obtener historial y datos del usuario desde MySQL
    historial_data = database.get_historial(usuario_id)
    pct_aciertos = database.get_pct_aciertos_global(usuario_id)

    if not historial_data:
        raise HTTPException(
            status_code=404,
            detail="No hay historial disponible para este usuario"
        )

    # Obtener nombre del usuario para el encabezado del reporte
    usuario_nombre = f"Usuario #{usuario_id}"
    try:
        conn = database.conectar()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT nombre FROM usuarios WHERE id = %s", (usuario_id,))
            row = cursor.fetchone()
            if row:
                usuario_nombre = row["nombre"]
            cursor.close()
            conn.close()
    except Exception:
        pass   # si falla la consulta se usa el nombre genérico

    # Generar texto plano del reporte
    texto_reporte = huffman.generar_texto_reporte(
        historial_data,
        usuario_nombre,
        pct_aciertos
    )

    # Aplicar compresión Huffman  O(n log n)
    resultado_huffman = huffman.comprimir_historial(texto_reporte)

    if not resultado_huffman:
        raise HTTPException(
            status_code=500, detail="Error al comprimir el historial")

    # Construir el archivo de salida:
    # Sección 1 → reporte legible original
    # Sección 2 → métricas académicas de compresión Huffman
    # Sección 3 → tabla de códigos binarios
    sep = "=" * 60

    metricas = (
        f"\n\n{sep}\n"
        f"  MÉTRICAS DE COMPRESIÓN — Algoritmo Huffman\n"
        f"  Complejidad: {resultado_huffman['complejidad']}\n"
        f"{sep}\n"
        f"  Símbolos únicos (n):   {resultado_huffman['simbolos_unicos']}\n"
        f"  Bits sin comprimir:    {resultado_huffman['bits_originales']} bits "
        f"({len(texto_reporte)} caracteres × 8 bits)\n"
        f"  Bits comprimidos:      {resultado_huffman['bits_comprimidos']} bits\n"
        f"  Tasa de compresión:    {resultado_huffman['tasa_compresion']}%\n"
        f"  Ahorro:                "
        f"{resultado_huffman['bits_originales'] - resultado_huffman['bits_comprimidos']} bits\n"
        f"{sep}\n"
        f"  TABLA DE CÓDIGOS HUFFMAN (ordenada por frecuencia):\n"
        f"  {'Símbolo':<10} {'Frecuencia':>10}  {'Código Binario'}\n"
        f"  {'-'*50}\n"
    )

    # Agregar tabla de códigos ordenada por frecuencia descendente
    tabla_codigos = sorted(
        resultado_huffman["frecuencias"].items(),
        key=lambda x: -x[1]
    )
    for simbolo, freq in tabla_codigos:
        nombre = repr(simbolo)
        codigo = resultado_huffman["codigos"][simbolo]
        metricas += f"  {nombre:<10} {freq:>10}  {codigo}\n"

    metricas += (
        f"{sep}\n"
        f"  BetDecision v2 — CompuPapus — IL355 CUCEI UdG 2026\n"
        f"{sep}\n"
    )

    contenido_final = texto_reporte + metricas

    # Devolver como archivo descargable
    return PlainTextResponse(
        content=contenido_final,
        headers={
            "Content-Disposition": f"attachment; filename=betdecision_historial_u{usuario_id}.txt",
            "Content-Type": "text/plain; charset=utf-8"
        }
    )


# ─────────────────────────────────────────────────────────────────────────────
# ARRANCAR EL SERVIDOR
# Ejecutar: uvicorn main:app --reload
# Docs:     http://localhost:8001/docs
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
