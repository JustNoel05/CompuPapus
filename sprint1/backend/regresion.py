# ─────────────────────────────────────────────────────────────────────────────
# regresion.py — BetDecision / CompuPapus
# Sprint 1 — Implementación de regresión lineal
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
# de que el equipo local gane.
# Positivo → favorece al local / Negativo → favorece al visitante
# ─────────────────────────────────────────────────────────────────────────────

PESOS = {
    "pct_victorias_local":     0.30,
    "pct_victorias_visitante": 0.25,
    "diferencial_goles_local": 0.15,
    "diferencial_goles_visit": 0.10,
    "forma_local":             0.10,
    "forma_visitante":         0.08,
    "tiros_arco_local":        0.05,
    "tiros_arco_visitante":    0.04,
    "posesion_local":          0.03,
    "intercepto":              0.50,   # base de probabilidad
}

# Apuesta base para calcular EV (en pesos)
APUESTA_BASE = 100
# Probabilidad mínima — evita recomendar resultados muy improbables
PROB_MINIMA = 25.0


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def calcular_momios():
    """
    Para cada partido de la jornada:
      1. Calcula probabilidades de local / empate / visitante con regresión lineal.
      2. Las normaliza para que sumen exactamente 100%.
      3. Convierte probabilidades a momios objetivos (momio = 1 / prob).
      4. Calcula el EV de cada opción y selecciona la recomendada.

    Retorna lista ordenada de mayor a menor EV del resultado recomendado.
    """
    resultados = []

    for partido in jornada:
        nombre_local     = partido["local"]
        nombre_visitante = partido["visitante"]

        local     = equipos[nombre_local]
        visitante = equipos[nombre_visitante]

        # ── Probabilidad de victoria LOCAL ────────────────────────────────
        p_local = (
            PESOS["intercepto"]
            + PESOS["pct_victorias_local"]     * get_pct_victorias_local(nombre_local)
            - PESOS["pct_victorias_visitante"] * get_pct_victorias_visitante(nombre_visitante)
            + PESOS["diferencial_goles_local"] * get_diferencial_goles(nombre_local)
            - PESOS["diferencial_goles_visit"] * get_diferencial_goles(nombre_visitante)
            + PESOS["forma_local"]             * get_forma_reciente(nombre_local)
            - PESOS["forma_visitante"]         * get_forma_reciente(nombre_visitante)
            + PESOS["tiros_arco_local"]        * (local["tiros_arco"] / 10)
            - PESOS["tiros_arco_visitante"]    * (visitante["tiros_arco"] / 10)
            + PESOS["posesion_local"]          * local["posesion"]
        )

        # ── Probabilidad de victoria VISITANTE ────────────────────────────
        p_visitante = (
            PESOS["intercepto"]
            + PESOS["pct_victorias_local"]     * get_pct_victorias_visitante(nombre_visitante)
            - PESOS["pct_victorias_visitante"] * get_pct_victorias_local(nombre_local)
            + PESOS["diferencial_goles_local"] * get_diferencial_goles(nombre_visitante)
            - PESOS["diferencial_goles_visit"] * get_diferencial_goles(nombre_local)
            + PESOS["forma_local"]             * get_forma_reciente(nombre_visitante)
            - PESOS["forma_visitante"]         * get_forma_reciente(nombre_local)
            + PESOS["tiros_arco_local"]        * (visitante["tiros_arco"] / 10)
            - PESOS["tiros_arco_visitante"]    * (local["tiros_arco"] / 10)
            + PESOS["posesion_local"]          * visitante["posesion"]
        )

        # ── Probabilidad de EMPATE ────────────────────────────────────────
        p_empate = 1 - p_local - p_visitante

        # ── Clamp mínimo al 5% para evitar momios infinitos ───────────────
        p_local     = max(0.05, p_local)
        p_empate    = max(0.05, p_empate)
        p_visitante = max(0.05, p_visitante)

        # ── Normalizar → suman exactamente 100% (sin sesgo de casa) ───────
        total        = p_local + p_empate + p_visitante
        p_local     /= total
        p_empate    /= total
        p_visitante /= total

        # ── Momios objetivos (momio = 1 / probabilidad) ───────────────────
        momio_local     = round(1 / p_local,     2)
        momio_empate    = round(1 / p_empate,    2)
        momio_visitante = round(1 / p_visitante, 2)

        # ── EV por opción ─────────────────────────────────────────────────
        # EV = P(ganar) × Ganancia_neta − P(perder) × Apuesta_base
        ev_local = round(
            p_local     * (momio_local     * APUESTA_BASE - APUESTA_BASE)
            - (1 - p_local)     * APUESTA_BASE, 2)

        ev_empate = round(
            p_empate    * (momio_empate    * APUESTA_BASE - APUESTA_BASE)
            - (1 - p_empate)    * APUESTA_BASE, 2)

        ev_visitante = round(
            p_visitante * (momio_visitante * APUESTA_BASE - APUESTA_BASE)
            - (1 - p_visitante) * APUESTA_BASE, 2)

        # ── Resultado recomendado (mayor EV) ─────────────────────────────
        opciones = [
            {"resultado": "Local",     "momio": momio_local,
             "prob": round(p_local * 100, 1),     "ev": ev_local},
            {"resultado": "Empate",    "momio": momio_empate,
             "prob": round(p_empate * 100, 1),    "ev": ev_empate},
            {"resultado": "Visitante", "momio": momio_visitante,
             "prob": round(p_visitante * 100, 1), "ev": ev_visitante},
        ]
        recomendado = max(opciones, key=lambda x: x["ev"])

        resultados.append({
            "local":      nombre_local,
            "visitante":  nombre_visitante,
            "momios": {
                "local":     {"momio": momio_local,     "prob": round(p_local * 100, 1)},
                "empate":    {"momio": momio_empate,    "prob": round(p_empate * 100, 1)},
                "visitante": {"momio": momio_visitante, "prob": round(p_visitante * 100, 1)},
            },
            "recomendado": recomendado,
            # Criterio: EV positivo Y probabilidad mínima del 25%
            "ev_positivo": recomendado["ev"] > 0 and recomendado["prob"] >= PROB_MINIMA
        })

    # Ordenar de mayor a menor EV del resultado recomendado
    return sorted(resultados, key=lambda x: x["recomendado"]["ev"], reverse=True)


# ─────────────────────────────────────────────────────────────────────────────
# Prueba de cálculo — Sprint 1
# Ejecutar: python regresion.py
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    partidos = calcular_momios()

    print("=" * 65)
    print("  BetDecision — Jornada 15 | Momios Objetivos y EV")
    print("=" * 65)

    suma_probs = []
    for i, p in enumerate(partidos, 1):
        m = p["momios"]
        r = p["recomendado"]
        ev_icon = "✓ EV+" if p["ev_positivo"] else "✗"

        # Verificar que las probabilidades suman 100%
        suma = m["local"]["prob"] + m["empate"]["prob"] + m["visitante"]["prob"]
        suma_probs.append(suma)

        print(f"\n{i}. {p['local']} vs {p['visitante']}")
        print(f"   Local:     momio {m['local']['momio']:5.2f}  ({m['local']['prob']:4.1f}%)")
        print(f"   Empate:    momio {m['empate']['momio']:5.2f}  ({m['empate']['prob']:4.1f}%)")
        print(f"   Visitante: momio {m['visitante']['momio']:5.2f}  ({m['visitante']['prob']:4.1f}%)")
        print(f"   Suma probs: {suma:.1f}%  ← debe ser ≈100%")
        print(f"   ── Recomendado: {r['resultado']:10} | "
              f"Momio: {r['momio']:.2f} | EV: {r['ev']:+.2f}  {ev_icon}")

    print("\n" + "=" * 65)
    ev_positivos = [p for p in partidos if p["ev_positivo"]]
    print(f"  Partidos con EV positivo: {len(ev_positivos)} de {len(partidos)}")
    print(f"  Promedio suma probabilidades: {sum(suma_probs)/len(suma_probs):.2f}% (debe ser ≈100%)")
    print("=" * 65)
