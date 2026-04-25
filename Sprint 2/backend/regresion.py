# ─────────────────────────────────────────────────────────────────────────────
# regresion.py — CompuPapus / BetDecision
# Regresión lineal con pesos manuales
# Calcula momios objetivos y EV por partido de la jornada
# ─────────────────────────────────────────────────────────────────────────────

from datos_equipos import (
    equipos, jornada,
    get_pct_victorias_local,
    get_pct_victorias_visitante,
    get_diferencial_goles,
    get_forma_reciente
)


# ─────────────────────────────────────────────────────────────────────────────
# PESOS DEL MODELO
# Cada peso representa cuánto influye esa variable en la probabilidad
# de que el equipo local gane el partido.
#
# Positivo → favorece al local
# Negativo → favorece al visitante
# ─────────────────────────────────────────────────────────────────────────────

PESOS = {
    "pct_victorias_local":     0.30,   # % victorias jugando de local
    "pct_victorias_visitante": 0.25,   # % victorias del visitante jugando fuera
    "diferencial_goles_local": 0.15,   # promedio GF-GC del local
    "diferencial_goles_visit": 0.10,   # promedio GF-GC del visitante
    "forma_local":             0.10,   # forma reciente del local (últimos 5)
    "forma_visitante":         0.08,   # forma reciente del visitante
    "tiros_arco_local":        0.05,   # presión ofensiva del local
    "tiros_arco_visitante":    0.04,   # presión ofensiva del visitante
    "posesion_local":          0.03,   # dominio del balón del local
    "intercepto":              0.50,   # base de probabilidad
}

# Apuesta base para calcular EV (en pesos)
APUESTA_BASE = 100
PROB_MINIMA = 25.0

# ─────────────────────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────


def calcular_momios():
    """
    Calcula los momios objetivos y EV de cada partido de la jornada.
    Devuelve una lista ordenada de mayor a menor EV del resultado recomendado.
    """
    resultados = []

    for partido in jornada:
        nombre_local = partido["local"]
        nombre_visitante = partido["visitante"]

        local = equipos[nombre_local]
        visitante = equipos[nombre_visitante]

        # ── Calcular probabilidad de victoria local ───────────────────────
        # Cada variable se multiplica por su peso y se suman al intercepto
        p_local = (
            PESOS["intercepto"]
            + PESOS["pct_victorias_local"] *
            get_pct_victorias_local(nombre_local)
            - PESOS["pct_victorias_visitante"] *
            get_pct_victorias_visitante(nombre_visitante)
            + PESOS["diferencial_goles_local"] *
            get_diferencial_goles(nombre_local)
            - PESOS["diferencial_goles_visit"] *
            get_diferencial_goles(nombre_visitante)
            + PESOS["forma_local"] * get_forma_reciente(nombre_local)
            - PESOS["forma_visitante"] * get_forma_reciente(nombre_visitante)
            + PESOS["tiros_arco_local"] * (local["tiros_arco"] / 10)
            - PESOS["tiros_arco_visitante"] * (visitante["tiros_arco"] / 10)
            + PESOS["posesion_local"] * local["posesion"]
        )

        # ── Calcular probabilidad de victoria visitante ───────────────────
        p_visitante = (
            PESOS["intercepto"]
            + PESOS["pct_victorias_local"] *
            get_pct_victorias_visitante(nombre_visitante)
            - PESOS["pct_victorias_visitante"] *
            get_pct_victorias_local(nombre_local)
            + PESOS["diferencial_goles_local"] *
            get_diferencial_goles(nombre_visitante)
            - PESOS["diferencial_goles_visit"] *
            get_diferencial_goles(nombre_local)
            + PESOS["forma_local"] * get_forma_reciente(nombre_visitante)
            - PESOS["forma_visitante"] * get_forma_reciente(nombre_local)
            + PESOS["tiros_arco_local"] * (visitante["tiros_arco"] / 10)
            - PESOS["tiros_arco_visitante"] * (local["tiros_arco"] / 10)
            + PESOS["posesion_local"] * visitante["posesion"]
        )

        # ── Probabilidad de empate ────────────────────────────────────────
        # El empate es lo que sobra después de local y visitante
        p_empate = 1 - p_local - p_visitante

        # ── Clamp: ninguna probabilidad puede ser menor a 0.05 (5%) ───────
        p_local = max(0.05, p_local)
        p_empate = max(0.05, p_empate)
        p_visitante = max(0.05, p_visitante)

        # ── Normalizar para que sumen exactamente 100% ────────────────────
        total = p_local + p_empate + p_visitante
        p_local /= total
        p_empate /= total
        p_visitante /= total

        # ── Convertir probabilidades a momios objetivos ───────────────────
        # Momio = 1 / probabilidad
        momio_local = round(1 / p_local,     2)
        momio_empate = round(1 / p_empate,    2)
        momio_visitante = round(1 / p_visitante, 2)

        # ── Calcular EV por opción ────────────────────────────────────────
        # EV = P(ganar) × Ganancia neta − P(perder) × Apuesta
        # Ganancia neta = momio × apuesta − apuesta
        ev_local = round(
            p_local * (momio_local * APUESTA_BASE - APUESTA_BASE)
            - (1 - p_local) * APUESTA_BASE, 2)

        ev_empate = round(
            p_empate * (momio_empate * APUESTA_BASE - APUESTA_BASE)
            - (1 - p_empate) * APUESTA_BASE, 2)

        ev_visitante = round(
            p_visitante * (momio_visitante * APUESTA_BASE - APUESTA_BASE)
            - (1 - p_visitante) * APUESTA_BASE, 2)

        # ── Seleccionar el resultado con mayor EV (recomendado) ───────────
        opciones = [
            {"resultado": "Local",     "momio": momio_local,
             "prob": round(p_local * 100, 1),     "ev": ev_local},
            {"resultado": "Empate",    "momio": momio_empate,
             "prob": round(p_empate * 100, 1),    "ev": ev_empate},
            {"resultado": "Visitante", "momio": momio_visitante,
             "prob": round(p_visitante * 100, 1), "ev": ev_visitante},
        ]
        recomendado = max(opciones, key=lambda x: x["ev"])

        # ── Armar resultado del partido ───────────────────────────────────
        resultados.append({
            "local":      nombre_local,
            "visitante":  nombre_visitante,
            "momios": {
                "local":     {"momio": momio_local,     "prob": round(p_local * 100, 1)},
                "empate":    {"momio": momio_empate,    "prob": round(p_empate * 100, 1)},
                "visitante": {"momio": momio_visitante, "prob": round(p_visitante * 100, 1)},
            },
            "recomendado": recomendado,

            "ev_positivo": recomendado["ev"] > 0 and recomendado["prob"] >= PROB_MINIMA
        })

    # Ordenar de mayor a menor EV del resultado recomendado
    return sorted(resultados, key=lambda x: x["recomendado"]["ev"], reverse=True)


# ─────────────────────────────────────────────────────────────────────────────
# PRUEBA — correr directamente para ver resultados
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    partidos = calcular_momios()

    print("=" * 65)
    print("  BetDecision — Jornada 15 | Momios Objetivos y EV")
    print("=" * 65)

    for i, p in enumerate(partidos, 1):
        m = p["momios"]
        r = p["recomendado"]
        ev_icon = "✓" if p["ev_positivo"] else "✗"

        print(f"\n{i}. {p['local']} vs {p['visitante']}")
        print(
            f"   Local:     momio {m['local']['momio']:5.2f}  ({m['local']['prob']:4.1f}%)")
        print(
            f"   Empate:    momio {m['empate']['momio']:5.2f}  ({m['empate']['prob']:4.1f}%)")
        print(
            f"   Visitante: momio {m['visitante']['momio']:5.2f}  ({m['visitante']['prob']:4.1f}%)")
        print(f"   ── Recomendado: {r['resultado']:10} | "
              f"Momio: {r['momio']:.2f} | "
              f"EV: {r['ev']:+.2f} {ev_icon}")

    print("\n" + "=" * 65)
    ev_positivos = [p for p in partidos if p["ev_positivo"]]
    print(
        f"  Partidos con EV positivo: {len(ev_positivos)} de {len(partidos)}")
    print("=" * 65)
