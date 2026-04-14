# ─────────────────────────────────────────────────────────────────────────────
# datos_equipos.py — BetDecision / CompuPapus
# Sprint 1 — Hardcodeo de datos históricos
# Dataset histórico Clausura 2026 — Actualizado a Jornada 14
# Formato historial: [resultado, goles_favor, goles_contra, local(1)/visitante(0)]
# W → Ganado   D → Empate   L → Perdido
# ─────────────────────────────────────────────────────────────────────────────

equipos = {

    "Cruz Azul": {
        "pos": 2, "gf_p": 1.9, "gc_p": 1.0, "posesion": 0.56,
        "tiros_arco": 6.5, "duelos": 0.512,
        "racha": ["D", "D", "L", "D", "W"],
        "descanso_ganando": 0.65,
        "historial": [
            ["D", 1, 1, 0], ["L", 1, 2, 1], ["D", 1, 1, 0],
            ["D", 2, 2, 0], ["W", 3, 0, 1], ["W", 2, 1, 0],
            ["W", 1, 0, 1], ["W", 2, 0, 0], ["W", 3, 2, 1], ["W", 1, 0, 0],
        ]
    },
    "Toluca": {
        "pos": 3, "gf_p": 1.6, "gc_p": 0.7, "posesion": 0.54,
        "tiros_arco": 5.3, "duelos": 0.508,
        "racha": ["D", "L", "D", "D", "W"],
        "descanso_ganando": 0.65,
        "historial": [
            ["D", 0, 0, 1], ["L", 0, 1, 0], ["D", 1, 1, 0],
            ["D", 1, 1, 1], ["W", 2, 0, 1], ["W", 1, 0, 0],
            ["W", 2, 1, 1], ["W", 1, 0, 0], ["W", 2, 1, 1], ["D", 0, 0, 0],
        ]
    },
    "Chivas": {
        "pos": 1, "gf_p": 1.6, "gc_p": 1.1, "posesion": 0.57,
        "tiros_arco": 4.9, "duelos": 0.530,
        "racha": ["L", "D", "W", "W", "W"],
        "descanso_ganando": 0.55,
        "historial": [
            ["L", 1, 4, 0], ["D", 2, 2, 1], ["W", 3, 2, 0],
            ["W", 3, 0, 1], ["W", 2, 1, 1], ["L", 1, 2, 0],
            ["L", 0, 2, 0], ["W", 2, 1, 1], ["W", 2, 0, 1], ["W", 1, 0, 0],
        ]
    },
    "Pachuca": {
        "pos": 4, "gf_p": 1.5, "gc_p": 0.8, "posesion": 0.52,
        "tiros_arco": 5.2, "duelos": 0.500,
        "racha": ["W", "W", "D", "D", "W"],
        "descanso_ganando": 0.55,
        "historial": [
            ["W", 2, 0, 1], ["W", 2, 1, 0], ["D", 1, 1, 1],
            ["D", 1, 1, 0], ["W", 1, 0, 1], ["W", 2, 1, 0],
            ["L", 0, 1, 0], ["W", 2, 0, 1], ["W", 1, 0, 1], ["L", 0, 2, 0],
        ]
    },
    "Pumas": {
        "pos": 4, "gf_p": 2.0, "gc_p": 1.1, "posesion": 0.50,
        "tiros_arco": 4.8, "duelos": 0.515,
        "racha": ["W", "D", "W", "D", "W"],
        "descanso_ganando": 0.50,
        "historial": [
            ["W", 3, 1, 1], ["D", 2, 2, 0], ["W", 1, 0, 1],
            ["D", 2, 2, 1], ["W", 2, 1, 1], ["L", 0, 1, 1],
            ["W", 1, 0, 0], ["D", 1, 1, 1], ["W", 2, 1, 0], ["L", 0, 1, 1],
        ]
    },
    "Tigres": {
        "pos": 7, "gf_p": 1.8, "gc_p": 1.1, "posesion": 0.54,
        "tiros_arco": 5.6, "duelos": 0.535,
        "racha": ["W", "W", "L", "L", "D"],
        "descanso_ganando": 0.50,
        "historial": [
            ["W", 4, 1, 1], ["L", 0, 1, 0], ["L", 1, 2, 0],
            ["D", 0, 0, 1], ["L", 1, 2, 0], ["L", 0, 1, 0],
            ["W", 2, 1, 1], ["L", 0, 1, 0], ["W", 3, 1, 1], ["L", 0, 1, 1],
        ]
    },
    "Atlas": {
        "pos": 6, "gf_p": 1.2, "gc_p": 1.3, "posesion": 0.47,
        "tiros_arco": 3.8, "duelos": 0.540,
        "racha": ["D", "L", "D", "L", "L"],
        "descanso_ganando": 0.30,
        "historial": [
            ["D", 0, 0, 1], ["L", 0, 2, 0], ["D", 0, 0, 1],
            ["D", 1, 1, 0], ["L", 1, 2, 0], ["L", 0, 1, 1],
            ["W", 1, 0, 0], ["L", 0, 2, 0], ["D", 1, 1, 1], ["L", 0, 1, 1],
        ]
    },
    "América": {
        "pos": 8, "gf_p": 1.1, "gc_p": 1.0, "posesion": 0.57,
        "tiros_arco": 5.1, "duelos": 0.520,
        "racha": ["D", "D", "L", "W", "W"],
        "descanso_ganando": 0.45,
        "historial": [
            ["D", 1, 1, 1], ["D", 1, 1, 0], ["L", 0, 1, 0],
            ["W", 2, 0, 1], ["W", 2, 0, 1], ["W", 1, 0, 0],
            ["L", 1, 2, 1], ["W", 1, 0, 1], ["L", 1, 2, 0], ["L", 0, 1, 1],
        ]
    },
    "Monterrey": {
        "pos": 13, "gf_p": 1.3, "gc_p": 1.4, "posesion": 0.58,
        "tiros_arco": 5.2, "duelos": 0.500,
        "racha": ["D", "L", "L", "D", "W"],
        "descanso_ganando": 0.35,
        "historial": [
            ["D", 0, 0, 1], ["L", 1, 2, 1], ["L", 2, 3, 1],
            ["D", 2, 2, 0], ["W", 3, 0, 1], ["W", 2, 1, 1],
            ["L", 0, 2, 0], ["D", 1, 1, 0], ["L", 0, 1, 0], ["D", 0, 0, 1],
        ]
    },
    "Puebla": {
        "pos": 15, "gf_p": 0.9, "gc_p": 1.4, "posesion": 0.43,
        "tiros_arco": 3.0, "duelos": 0.455,
        "racha": ["L", "D", "L", "D", "L"],
        "descanso_ganando": 0.25,
        "historial": [
            ["L", 0, 1, 1], ["D", 1, 1, 0], ["L", 1, 2, 0],
            ["D", 0, 0, 1], ["L", 0, 1, 0], ["W", 1, 0, 1],
            ["L", 0, 2, 1], ["L", 0, 2, 0], ["D", 1, 1, 1], ["L", 1, 2, 0],
        ]
    },
    "Atl.SanLuis": {
        "pos": 10, "gf_p": 1.6, "gc_p": 1.6, "posesion": 0.48,
        "tiros_arco": 3.9, "duelos": 0.485,
        "racha": ["D", "W", "W", "D", "L"],
        "descanso_ganando": 0.35,
        "historial": [
            ["D", 0, 0, 0], ["W", 2, 1, 0], ["W", 2, 1, 0],
            ["D", 1, 1, 1], ["L", 1, 2, 1], ["W", 3, 2, 1],
            ["L", 1, 3, 0], ["L", 0, 1, 0], ["D", 1, 1, 1], ["L", 0, 1, 1],
        ]
    },
    "Juárez": {
        "pos": 11, "gf_p": 1.4, "gc_p": 1.5, "posesion": 0.43,
        "tiros_arco": 3.3, "duelos": 0.478,
        "racha": ["L", "D", "W", "D", "D"],
        "descanso_ganando": 0.25,
        "historial": [
            ["L", 0, 1, 1], ["D", 1, 1, 0], ["W", 2, 1, 1],
            ["D", 2, 2, 1], ["L", 0, 2, 0], ["L", 0, 1, 1],
            ["L", 0, 3, 0], ["D", 2, 2, 1], ["L", 1, 2, 0], ["W", 1, 0, 0],
        ]
    },
    "León": {
        "pos": 8, "gf_p": 1.1, "gc_p": 1.4, "posesion": 0.50,
        "tiros_arco": 4.2, "duelos": 0.500,
        "racha": ["W", "W", "L", "L", "L"],
        "descanso_ganando": 0.35,
        "historial": [
            ["W", 1, 0, 0], ["W", 2, 0, 1], ["L", 1, 2, 0],
            ["L", 0, 3, 1], ["L", 1, 2, 0], ["W", 1, 0, 1],
            ["W", 2, 1, 0], ["D", 1, 1, 1], ["L", 2, 3, 0], ["L", 1, 2, 1],
        ]
    },
    "Mazatlán": {
        "pos": 17, "gf_p": 1.1, "gc_p": 2.2, "posesion": 0.46,
        "tiros_arco": 3.2, "duelos": 0.482,
        "racha": ["L", "L", "L", "L", "D"],
        "descanso_ganando": 0.15,
        "historial": [
            ["L", 1, 3, 0], ["L", 1, 2, 0], ["D", 1, 1, 1],
            ["L", 0, 2, 0], ["D", 1, 1, 1], ["L", 0, 1, 0],
            ["L", 1, 2, 0], ["D", 0, 0, 1], ["W", 2, 1, 1], ["L", 0, 1, 0],
        ]
    },
    "Tijuana": {
        "pos": 9, "gf_p": 1.2, "gc_p": 1.0, "posesion": 0.47,
        "tiros_arco": 3.8, "duelos": 0.482,
        "racha": ["W", "W", "W", "D", "D"],
        "descanso_ganando": 0.35,
        "historial": [
            ["W", 1, 0, 1], ["W", 1, 0, 1], ["W", 3, 0, 0],
            ["D", 0, 0, 1], ["D", 1, 1, 0], ["D", 1, 1, 1],
            ["L", 1, 2, 0], ["D", 0, 0, 1], ["L", 0, 2, 1], ["L", 0, 1, 1],
        ]
    },
    "Necaxa": {
        "pos": 12, "gf_p": 1.1, "gc_p": 1.4, "posesion": 0.45,
        "tiros_arco": 3.5, "duelos": 0.488,
        "racha": ["L", "W", "W", "D", "W"],
        "descanso_ganando": 0.30,
        "historial": [
            ["L", 1, 3, 0], ["W", 2, 1, 1], ["W", 3, 0, 1],
            ["D", 0, 0, 0], ["L", 1, 2, 0], ["L", 1, 2, 1],
            ["W", 2, 1, 1], ["D", 1, 1, 1], ["W", 1, 0, 0], ["W", 1, 0, 0],
        ]
    },
    "Querétaro": {
        "pos": 16, "gf_p": 0.9, "gc_p": 1.5, "posesion": 0.44,
        "tiros_arco": 3.3, "duelos": 0.470,
        "racha": ["W", "W", "D", "L", "W"],
        "descanso_ganando": 0.25,
        "historial": [
            ["W", 3, 1, 1], ["W", 1, 0, 1], ["D", 0, 0, 0],
            ["D", 0, 0, 0], ["L", 0, 2, 0], ["W", 1, 0, 1],
            ["L", 0, 1, 1], ["L", 0, 2, 0], ["L", 0, 1, 1], ["D", 1, 1, 0],
        ]
    },
    "Santos": {
        "pos": 18, "gf_p": 1.1, "gc_p": 2.4, "posesion": 0.48,
        "tiros_arco": 4.0, "duelos": 0.482,
        "racha": ["L", "D", "W", "L", "L"],
        "descanso_ganando": 0.15,
        "historial": [
            ["L", 0, 2, 0], ["D", 1, 1, 1], ["W", 2, 1, 1],
            ["L", 0, 3, 0], ["L", 0, 3, 0], ["L", 2, 3, 0],
            ["D", 2, 2, 0], ["D", 0, 0, 0], ["D", 1, 1, 0], ["D", 1, 1, 1],
        ]
    },
    "Guadalajara": {
        "pos": 1, "gf_p": 1.9, "gc_p": 1.0, "posesion": 0.53,
        "tiros_arco": 5.0, "duelos": 0.518,
        "racha": ["L", "D", "W", "W", "W"],
        "descanso_ganando": 0.60,
        "historial": [
            ["L", 1, 4, 0], ["D", 2, 2, 1], ["W", 3, 2, 0],
            ["W", 3, 0, 1], ["W", 2, 1, 1], ["W", 2, 1, 0],
            ["W", 1, 0, 1], ["W", 2, 0, 1], ["W", 2, 1, 1], ["W", 1, 0, 0],
        ]
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Jornada 15 — Clausura 2026  (hardcodeada)
# ─────────────────────────────────────────────────────────────────────────────

jornada = [
    {"local": "Atl.SanLuis",  "visitante": "Pumas"},
    {"local": "Mazatlán",     "visitante": "Querétaro"},
    {"local": "Necaxa",       "visitante": "Tigres"},
    {"local": "Cruz Azul",    "visitante": "Tijuana"},
    {"local": "Guadalajara",  "visitante": "Puebla"},
    {"local": "Monterrey",    "visitante": "Pachuca"},
    {"local": "León",         "visitante": "Juárez"},
    {"local": "América",      "visitante": "Toluca"},
    {"local": "Santos",       "visitante": "Atlas"},
]


# ─────────────────────────────────────────────────────────────────────────────
# Funciones auxiliares — usadas por regresion.py
# ─────────────────────────────────────────────────────────────────────────────

def get_pct_victorias_local(equipo):
    h = equipos[equipo]["historial"]
    locales = [p for p in h if p[3] == 1]
    if not locales:
        return 0
    return sum(1 for p in locales if p[0] == "W") / len(locales)


def get_pct_victorias_visitante(equipo):
    h = equipos[equipo]["historial"]
    visitantes = [p for p in h if p[3] == 0]
    if not visitantes:
        return 0
    return sum(1 for p in visitantes if p[0] == "W") / len(visitantes)


def get_diferencial_goles(equipo):
    h = equipos[equipo]["historial"]
    return sum(p[1] - p[2] for p in h) / len(h)


def get_forma_reciente(equipo):
    puntos = {"W": 3, "D": 1, "L": 0}
    return sum(puntos[r] for r in equipos[equipo]["racha"]) / 15


# ─────────────────────────────────────────────────────────────────────────────
# Prueba rápida
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Equipos cargados: {len(equipos)}")
    print(f"Partidos jornada 15: {len(jornada)}")
    for p in jornada:
        print(f"  {p['local']:15} vs {p['visitante']}")
