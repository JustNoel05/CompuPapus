# ─────────────────────────────────────────────────────────────────────────────
# datos_equipos.py — CompuPapus / BetDecision
# Dataset histórico Clausura 2026 — Actualizado a Jornada 14
# Historial formato: [resultado, goles_favor, goles_contra, local(1)/visitante(0)]
# ─────────────────────────────────────────────────────────────────────────────

# W → Won / Ganado   D → Draw / Empate   L → Lost / Perdido

equipos = {

    "Cruz Azul": {
        "pos": 2, "gf_p": 1.9, "gc_p": 1.0, "posesion": 0.56,
        "tiros_arco": 6.5, "duelos": 0.512,
        "racha": ["D", "D", "L", "D", "W"],
        "descanso_ganando": 0.65,
        "historial": [
            ["D", 1, 1, 0],  # J14 vs América     (Visitante)
            ["L", 1, 2, 1],  # J13 vs Pachuca      (Local)
            ["D", 1, 1, 0],  # J12 vs Mazatlán     (Visitante)
            ["D", 2, 2, 0],  # J11 vs Pumas        (Visitante)
            ["W", 3, 0, 1],  # J10 vs Santos       (Local)
            ["W", 2, 1, 0],  # J9  vs Atl.SanLuis  (Visitante)
            ["W", 1, 0, 1],  # J8  vs Monterrey    (Local)
            ["W", 2, 0, 0],  # J7  vs Puebla       (Visitante)
            ["W", 3, 2, 1],  # J6  vs León         (Local)
            ["W", 1, 0, 0],  # J5  vs Tijuana      (Visitante)
        ]
    },

    "Toluca": {
        "pos": 3, "gf_p": 1.6, "gc_p": 0.7, "posesion": 0.54,
        "tiros_arco": 5.3, "duelos": 0.508,
        "racha": ["D", "L", "D", "D", "W"],
        "descanso_ganando": 0.65,
        "historial": [
            # J14 vs Atl.SanLuis  (pendiente/empate referencia)
            ["D", 0, 0, 1],
            ["L", 0, 1, 0],  # J13 vs Querétaro    (Visitante)
            ["D", 1, 1, 0],  # J12 vs Pachuca      (Visitante)
            ["D", 1, 1, 1],  # J11 vs Atlas        (Local)
            ["W", 2, 0, 1],  # J10 vs Juárez       (Local)
            ["W", 1, 0, 0],  # J9  vs Pumas        (Visitante)
            ["W", 2, 1, 1],  # J8  vs Guadalajara  (Local)
            ["W", 1, 0, 0],  # J7  vs Tigres       (Visitante)
            ["W", 2, 1, 1],  # J6  vs América      (Local)
            ["D", 0, 0, 0],  # J5  vs Monterrey    (Visitante)
        ]
    },

    "Chivas": {
        "pos": 1, "gf_p": 1.6, "gc_p": 1.1, "posesion": 0.57,
        "tiros_arco": 4.9, "duelos": 0.530,
        "racha": ["L", "D", "W", "W", "W"],
        "descanso_ganando": 0.55,
        "historial": [
            ["L", 1, 4, 0],  # J14 vs Tigres       (Visitante)
            ["D", 2, 2, 1],  # J13 vs Pumas        (Local)
            ["W", 3, 2, 0],  # J12 vs Monterrey    (Visitante)
            ["W", 3, 0, 1],  # J11 vs Santos       (Local)
            ["W", 2, 1, 1],  # J10 vs Atlas        (Local)
            ["L", 1, 2, 0],  # J9  vs Toluca       (Visitante)
            ["L", 0, 2, 0],  # J8  vs Cruz Azul    (Visitante)
            ["W", 2, 1, 1],  # J7  vs Monterrey    (Local)
            ["W", 2, 0, 1],  # J6  vs Puebla       (Local)
            ["W", 1, 0, 0],  # J5  vs América      (Visitante)
        ]
    },

    "Pachuca": {
        "pos": 4, "gf_p": 1.5, "gc_p": 0.8, "posesion": 0.52,
        "tiros_arco": 5.2, "duelos": 0.500,
        "racha": ["W", "W", "D", "D", "W"],
        "descanso_ganando": 0.55,
        "historial": [
            ["W", 2, 0, 1],  # J14 vs Santos       (Local)
            ["W", 2, 1, 0],  # J13 vs Cruz Azul    (Visitante)
            ["D", 1, 1, 1],  # J12 vs Toluca       (Local)
            ["D", 1, 1, 0],  # J11 vs Atl.SanLuis  (Visitante)
            ["W", 1, 0, 1],  # J10 vs Puebla       (Local)
            ["W", 2, 1, 0],  # J9  vs Necaxa       (Visitante)
            ["L", 0, 1, 0],  # J8  vs Cruz Azul    (Visitante)
            ["W", 2, 0, 1],  # J7  vs Monterrey    (Local)
            ["W", 1, 0, 1],  # J6  vs América      (Local)
            ["L", 0, 2, 0],  # J5  vs Toluca       (Visitante)
        ]
    },

    "Pumas": {
        "pos": 4, "gf_p": 2.0, "gc_p": 1.1, "posesion": 0.50,
        "tiros_arco": 4.8, "duelos": 0.515,
        "racha": ["W", "D", "W", "D", "W"],
        "descanso_ganando": 0.50,
        "historial": [
            ["W", 3, 1, 1],  # J14 vs Mazatlán     (Local)
            ["D", 2, 2, 0],  # J13 vs Chivas       (Visitante)
            ["W", 1, 0, 1],  # J12 vs América      (Local)
            ["D", 2, 2, 1],  # J11 vs Cruz Azul    (Local)
            ["W", 2, 1, 1],  # J10 vs Necaxa       (Local)
            ["L", 0, 1, 1],  # J9  vs Toluca       (Local)
            ["W", 1, 0, 0],  # J8  vs Atlas        (Visitante)
            ["D", 1, 1, 1],  # J7  vs Monterrey    (Local)
            ["W", 2, 1, 0],  # J6  vs León         (Visitante)
            ["L", 0, 1, 1],  # J5  vs Pachuca      (Local)
        ]
    },

    "Tigres": {
        "pos": 7, "gf_p": 1.8, "gc_p": 1.1, "posesion": 0.54,
        "tiros_arco": 5.6, "duelos": 0.535,
        "racha": ["W", "W", "L", "L", "D"],
        "descanso_ganando": 0.50,
        "historial": [
            ["W", 4, 1, 1],  # J14 vs Chivas       (Local)
            ["L", 0, 1, 0],  # J13 vs Tijuana      (Local)
            ["L", 1, 2, 0],  # J12 vs Juárez       (Visitante)
            ["D", 0, 0, 1],  # J11 vs Querétaro    (Local)
            ["L", 1, 2, 0],  # J10 vs Monterrey    (Visitante)
            ["L", 0, 1, 0],  # J9  vs Puebla       (Visitante)
            ["W", 2, 1, 1],  # J8  vs León         (Local)
            ["L", 0, 1, 0],  # J7  vs América      (Visitante)
            ["W", 3, 1, 1],  # J6  vs Atl.SanLuis  (Local)
            ["L", 0, 1, 1],  # J5  vs Toluca       (Local)
        ]
    },

    "Atlas": {
        "pos": 6, "gf_p": 1.2, "gc_p": 1.3, "posesion": 0.47,
        "tiros_arco": 3.8, "duelos": 0.540,
        "racha": ["D", "L", "D", "L", "L"],
        "descanso_ganando": 0.30,
        "historial": [
            ["D", 0, 0, 1],  # J14 vs Monterrey    (Visitante)
            ["L", 0, 2, 0],  # J13 vs León         (Local)
            ["D", 0, 0, 1],  # J12 vs Querétaro    (Local)
            ["D", 1, 1, 0],  # J11 vs Toluca       (Visitante)
            ["L", 1, 2, 0],  # J10 vs Guadalajara  (Visitante)
            ["L", 0, 1, 1],  # J9  vs Pumas        (Local)
            ["W", 1, 0, 0],  # J8  vs Querétaro    (Visitante)
            ["L", 0, 2, 0],  # J7  vs Pachuca      (Visitante)
            ["D", 1, 1, 1],  # J6  vs Santos       (Local)
            ["L", 0, 1, 1],  # J5  vs Necaxa       (Local)
        ]
    },

    "América": {
        "pos": 8, "gf_p": 1.1, "gc_p": 1.0, "posesion": 0.57,
        "tiros_arco": 5.1, "duelos": 0.520,
        "racha": ["D", "D", "L", "W", "W"],
        "descanso_ganando": 0.45,
        "historial": [
            ["D", 1, 1, 1],  # J14 vs Cruz Azul    (Local)
            ["D", 1, 1, 0],  # J13 vs Santos       (Visitante)
            ["L", 0, 1, 0],  # J12 vs Pumas        (Visitante)
            ["W", 2, 0, 1],  # J11 vs Mazatlán     (Local)
            ["W", 2, 0, 1],  # J10 vs Querétaro    (Local)
            ["W", 1, 0, 0],  # J9  vs Juárez       (Visitante)
            ["L", 1, 2, 1],  # J8  vs Monterrey    (Local)
            ["W", 1, 0, 1],  # J7  vs Tigres       (Local)
            ["L", 1, 2, 0],  # J6  vs Toluca       (Visitante)
            ["L", 0, 1, 1],  # J5  vs Guadalajara  (Local)
        ]
    },

    "Monterrey": {
        "pos": 13, "gf_p": 1.3, "gc_p": 1.4, "posesion": 0.58,
        "tiros_arco": 5.2, "duelos": 0.500,
        "racha": ["D", "L", "L", "D", "W"],
        "descanso_ganando": 0.35,
        "historial": [
            ["D", 0, 0, 1],  # J14 vs Atlas        (Local)
            ["L", 1, 2, 1],  # J13 vs Atl.SanLuis  (Local)
            ["L", 2, 3, 1],  # J12 vs Chivas       (Local)
            ["D", 2, 2, 0],  # J11 vs Juárez       (Visitante)
            ["W", 3, 0, 1],  # J10 vs Juárez       (Local)
            ["W", 2, 1, 1],  # J9  vs Tigres       (Local)
            ["L", 0, 2, 0],  # J8  vs Pachuca      (Visitante)
            ["D", 1, 1, 0],  # J7  vs Pumas        (Visitante)
            ["L", 0, 1, 0],  # J6  vs Cruz Azul    (Visitante)
            ["D", 0, 0, 1],  # J5  vs Toluca       (Local)
        ]
    },

    "Puebla": {
        "pos": 15, "gf_p": 0.9, "gc_p": 1.4, "posesion": 0.43,
        "tiros_arco": 3.0, "duelos": 0.455,
        "racha": ["L", "D", "L", "D", "L"],
        "descanso_ganando": 0.25,
        "historial": [
            ["L", 0, 1, 1],  # J14 vs León         (Local)
            ["D", 1, 1, 0],  # J13 vs Juárez       (Local)
            ["L", 1, 2, 0],  # J12 vs Santos       (Visitante)
            ["D", 0, 0, 1],  # J11 vs Necaxa       (Local)
            ["L", 0, 1, 0],  # J10 vs Pachuca      (Visitante)
            ["W", 1, 0, 1],  # J9  vs Tigres       (Local)
            ["L", 0, 2, 1],  # J8  vs Cruz Azul    (Local)
            ["L", 0, 2, 0],  # J7  vs Guadalajara  (Visitante)
            ["D", 1, 1, 1],  # J6  vs Atl.SanLuis  (Local)
            ["L", 1, 2, 0],  # J5  vs Necaxa       (Visitante)
        ]
    },

    "Atl.SanLuis": {
        "pos": 10, "gf_p": 1.6, "gc_p": 1.6, "posesion": 0.48,
        "tiros_arco": 3.9, "duelos": 0.485,
        "racha": ["D", "W", "W", "D", "L"],
        "descanso_ganando": 0.35,
        "historial": [
            ["D", 0, 0, 0],  # J14 vs Toluca       (Visitante pendiente)
            ["W", 2, 1, 0],  # J13 vs Monterrey    (Visitante)
            ["W", 2, 1, 0],  # J12 vs León         (Local)
            ["D", 1, 1, 1],  # J11 vs Pachuca      (Local)
            ["L", 1, 2, 1],  # J10 vs Cruz Azul    (Local)
            ["W", 3, 2, 1],  # J9  vs Santos       (Local)
            ["L", 1, 3, 0],  # J8  vs Tigres       (Visitante)
            ["L", 0, 1, 0],  # J7  vs América      (Visitante)
            ["D", 1, 1, 1],  # J6  vs Pachuca      (Local)
            ["L", 0, 1, 1],  # J5  vs Juárez       (Local)
        ]
    },

    "Juárez": {
        "pos": 11, "gf_p": 1.4, "gc_p": 1.5, "posesion": 0.43,
        "tiros_arco": 3.3, "duelos": 0.478,
        "racha": ["L", "D", "W", "D", "D"],
        "descanso_ganando": 0.25,
        "historial": [
            ["L", 0, 1, 1],  # J14 vs Tijuana      (Local)
            ["D", 1, 1, 0],  # J13 vs Puebla       (Visitante)
            ["W", 2, 1, 1],  # J12 vs Tigres       (Local)
            ["D", 2, 2, 1],  # J11 vs Monterrey    (Local)
            ["L", 0, 2, 0],  # J10 vs Toluca       (Visitante)
            ["L", 0, 1, 1],  # J9  vs América      (Local)
            ["L", 0, 3, 0],  # J8  vs Monterrey    (Visitante)
            ["D", 2, 2, 1],  # J7  vs Santos       (Local)
            ["L", 1, 2, 0],  # J6  vs Tigres       (Visitante)
            ["W", 1, 0, 0],  # J5  vs Atl.SanLuis  (Visitante)
        ]
    },

    "León": {
        "pos": 8, "gf_p": 1.1, "gc_p": 1.4, "posesion": 0.50,
        "tiros_arco": 4.2, "duelos": 0.500,
        "racha": ["W", "W", "L", "L", "L"],
        "descanso_ganando": 0.35,
        "historial": [
            ["W", 1, 0, 0],  # J14 vs Puebla       (Visitante)
            ["W", 2, 0, 1],  # J13 vs Atlas        (Local)
            ["L", 1, 2, 0],  # J12 vs Atl.SanLuis  (Visitante)
            ["L", 0, 3, 1],  # J11 vs Tijuana      (Local)
            ["L", 1, 2, 0],  # J10 vs Tigres       (Visitante)
            ["W", 1, 0, 1],  # J9  vs Necaxa       (Local)
            ["W", 2, 1, 0],  # J8  vs Querétaro    (Visitante)
            ["D", 1, 1, 1],  # J7  vs Santos       (Local)
            ["L", 2, 3, 0],  # J6  vs Cruz Azul    (Visitante)
            ["L", 1, 2, 1],  # J5  vs Pumas        (Local)
        ]
    },

    "Mazatlán": {
        "pos": 17, "gf_p": 1.1, "gc_p": 2.2, "posesion": 0.46,
        "tiros_arco": 3.2, "duelos": 0.482,
        "racha": ["L", "L", "L", "L", "D"],
        "descanso_ganando": 0.15,
        "historial": [
            ["L", 1, 3, 0],  # J14 vs Pumas        (Visitante)
            ["L", 1, 2, 0],  # J13 vs Necaxa       (Visitante)
            ["D", 1, 1, 1],  # J12 vs Cruz Azul    (Local)
            ["L", 0, 2, 0],  # J11 vs América      (Visitante)
            ["D", 1, 1, 1],  # J10 vs Tijuana      (Local)
            ["L", 0, 1, 0],  # J9  vs Querétaro    (Visitante)
            ["L", 1, 2, 0],  # J8  vs Necaxa       (Visitante)
            ["D", 0, 0, 1],  # J7  vs Santos       (Local)
            ["W", 2, 1, 1],  # J6  vs Puebla       (Local)
            ["L", 0, 1, 0],  # J5  vs Atl.SanLuis  (Visitante)
        ]
    },

    "Tijuana": {
        "pos": 9, "gf_p": 1.2, "gc_p": 1.0, "posesion": 0.47,
        "tiros_arco": 3.8, "duelos": 0.482,
        "racha": ["W", "W", "W", "D", "D"],
        "descanso_ganando": 0.35,
        "historial": [
            ["W", 1, 0, 1],  # J14 vs Juárez       (Visitante)
            ["W", 1, 0, 1],  # J13 vs Tigres       (Visitante)
            ["W", 3, 0, 0],  # J12 vs León         (Visitante)
            # J11 vs Querétaro    (Local→ en realidad visitante vs Tigres)
            ["D", 0, 0, 1],
            ["D", 1, 1, 0],  # J10 vs Mazatlán     (Visitante)
            ["D", 1, 1, 1],  # J9  vs América      (Local)
            ["L", 1, 2, 0],  # J8  vs Guadalajara  (Visitante)
            ["D", 0, 0, 1],  # J7  vs Pumas        (Local)
            ["L", 0, 2, 1],  # J6  vs Tigres       (Local)
            ["L", 0, 1, 1],  # J5  vs Cruz Azul    (Local)
        ]
    },

    "Necaxa": {
        "pos": 12, "gf_p": 1.1, "gc_p": 1.4, "posesion": 0.45,
        "tiros_arco": 3.5, "duelos": 0.488,
        "racha": ["L", "W", "W", "D", "W"],
        "descanso_ganando": 0.30,
        "historial": [
            ["L", 1, 3, 0],  # J14 vs Querétaro    (Local)
            ["W", 2, 1, 1],  # J13 vs Mazatlán     (Local)
            ["W", 3, 0, 1],  # J12 vs Tijuana      (Local)
            ["D", 0, 0, 0],  # J11 vs Puebla       (Visitante)
            ["L", 1, 2, 0],  # J10 vs Pumas        (Visitante)
            ["L", 1, 2, 1],  # J9  vs Pachuca      (Local)
            ["W", 2, 1, 1],  # J8  vs Mazatlán     (Local)
            ["D", 1, 1, 1],  # J7  vs Tijuana      (Local)
            ["W", 1, 0, 0],  # J6  vs Querétaro    (Visitante)
            ["W", 1, 0, 0],  # J5  vs Atlas        (Visitante)
        ]
    },

    "Querétaro": {
        "pos": 16, "gf_p": 0.9, "gc_p": 1.5, "posesion": 0.44,
        "tiros_arco": 3.3, "duelos": 0.470,
        "racha": ["W", "W", "D", "L", "W"],
        "descanso_ganando": 0.25,
        "historial": [
            ["W", 3, 1, 1],  # J14 vs Necaxa       (Visitante)
            ["W", 1, 0, 1],  # J13 vs Toluca       (Local)
            ["D", 0, 0, 0],  # J12 vs Atlas        (Visitante)
            ["D", 0, 0, 0],  # J11 vs Tigres       (Visitante)
            ["L", 0, 2, 0],  # J10 vs América      (Visitante)
            ["W", 1, 0, 1],  # J9  vs Mazatlán     (Local)
            ["L", 0, 1, 1],  # J8  vs Atlas        (Local)
            ["L", 0, 2, 0],  # J7  vs Guadalajara  (Visitante)
            ["L", 0, 1, 1],  # J6  vs Necaxa       (Local)
            ["D", 1, 1, 0],  # J5  vs Santos       (Visitante)
        ]
    },

    "Santos": {
        "pos": 18, "gf_p": 1.1, "gc_p": 2.4, "posesion": 0.48,
        "tiros_arco": 4.0, "duelos": 0.482,
        "racha": ["L", "D", "W", "L", "L"],
        "descanso_ganando": 0.15,
        "historial": [
            ["L", 0, 2, 0],  # J14 vs Pachuca      (Visitante)
            ["D", 1, 1, 1],  # J13 vs América      (Local)
            ["W", 2, 1, 1],  # J12 vs Puebla       (Local)
            ["L", 0, 3, 0],  # J11 vs Guadalajara  (Visitante)
            ["L", 0, 3, 0],  # J10 vs Cruz Azul    (Visitante)
            ["L", 2, 3, 0],  # J9  vs Atl.SanLuis  (Visitante)
            ["D", 2, 2, 0],  # J8  vs Juárez       (Visitante)
            ["D", 0, 0, 0],  # J7  vs Mazatlán     (Visitante)
            ["D", 1, 1, 0],  # J6  vs Atlas        (Visitante)
            ["D", 1, 1, 1],  # J5  vs Querétaro    (Local)
        ]
    },

    "Guadalajara": {
        "pos": 1, "gf_p": 1.9, "gc_p": 1.0, "posesion": 0.53,
        "tiros_arco": 5.0, "duelos": 0.518,
        "racha": ["L", "D", "W", "W", "W"],
        "descanso_ganando": 0.60,
        "historial": [
            ["L", 1, 4, 0],  # J14 vs Tigres       (Visitante)
            ["D", 2, 2, 1],  # J13 vs Pumas        (Local)
            ["W", 3, 2, 0],  # J12 vs Monterrey    (Visitante)
            ["W", 3, 0, 1],  # J11 vs Santos       (Local)
            ["W", 2, 1, 1],  # J10 vs Atlas        (Local)
            ["W", 2, 1, 0],  # J9  vs Toluca       (Visitante)
            ["W", 1, 0, 1],  # J8  vs Cruz Azul    (Local)
            ["W", 2, 0, 1],  # J7  vs Puebla       (Local)
            ["W", 2, 1, 1],  # J6  vs América      (Local)
            ["W", 1, 0, 0],  # J5  vs Monterrey    (Visitante)
        ]
    },

}

# ─────────────────────────────────────────────────────────────────────────────
# Jornada 15 — Clausura 2026
# Del 17 al 20 de abril de 2026
# ─────────────────────────────────────────────────────────────────────────────

jornada = [
    {"local": "Atl.SanLuis",  "visitante": "Pumas"},      # Vie 17
    {"local": "Mazatlán",     "visitante": "Querétaro"},  # Vie 17
    {"local": "Necaxa",       "visitante": "Tigres"},     # Vie 17
    {"local": "Cruz Azul",    "visitante": "Tijuana"},    # Sáb 18
    {"local": "Guadalajara",  "visitante": "Puebla"},     # Sáb 18
    {"local": "Monterrey",    "visitante": "Pachuca"},    # Sáb 18
    {"local": "León",         "visitante": "Juárez"},     # Sáb 18
    {"local": "América",      "visitante": "Toluca"},     # Sáb 18
    {"local": "Santos",       "visitante": "Atlas"},      # Dom 19
]


# ─────────────────────────────────────────────────────────────────────────────
# Funciones auxiliares
# ─────────────────────────────────────────────────────────────────────────────

def get_pct_victorias(equipo):
    h = equipos[equipo]["historial"]
    return sum(1 for p in h if p[0] == "W") / len(h)


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


if __name__ == "__main__":
    print("=== BetDecision — Dataset cargado ===")
    print(f"Equipos: {len(equipos)}")
    print(f"Partidos jornada 15: {len(jornada)}")
    print()
    for partido in jornada:
        l = partido["local"]
        v = partido["visitante"]
        print(f"{l:15} vs {v:15} | "
              f"Forma local: {get_forma_reciente(l):.2f} | "
              f"Forma visit: {get_forma_reciente(v):.2f}")
