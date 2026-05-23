# ─────────────────────────────────────────────────────────────────────────────
# datos_equipos.py — CompuPapus / BetDecision
# Dataset histórico Clausura 2026 — Actualizado a Final
# Historial acumulado de toda la liguilla incorporado
#
# Cuartos ida:    Atlas 2-3 Cruz Azul | Tigres 3-1 Chivas | América 3-3 Pumas | Toluca 0-1 Pachuca
# Cuartos vuelta: Cruz Azul 1-0 Atlas | Chivas 2-0 Tigres | Pumas 3-3 América | Pachuca 2-0 Toluca
# Semis ida:      Pachuca 1-0 Pumas   | Cruz Azul 2-2 Chivas
# Semis vuelta:   Pumas 1-0 Pachuca   | Chivas 1-2 Cruz Azul
#
# Finalistas: Pumas (1°) vs Cruz Azul (3°)
# Jornada activa: FINAL Clausura 2026
#   Ida:   Jue 21 may — Estadio Cuauhtémoc, Puebla (Cruz Azul local por venue FIFA)
#   Vuelta:Dom 24 may — Estadio Olímpico Universitario (Pumas local)
# Historial formato: [resultado, goles_favor, goles_contra, local(1)/visitante(0)]
# ─────────────────────────────────────────────────────────────────────────────

# W → Won / Ganado   D → Draw / Empate   L → Lost / Perdido

equipos = {

    # ─────────────────────────────────────────────────────────────────────────
    # PUMAS — 1° tabla | Líder general | 15 años sin título
    # Eliminó a América (6-6 global, mejor pos.) y Pachuca (1-1 global, mejor pos.)
    # Keylor Navas determinante | Efraín Juárez busca su primer título
    # Final ida: visitante en Puebla | Vuelta: local en CU
    # ─────────────────────────────────────────────────────────────────────────
    "Pumas": {
        "pos": 1, "gf_p": 2.1, "gc_p": 0.9, "posesion": 0.51,
        "tiros_arco": 5.3, "duelos": 0.518,
        "racha": ["W", "D", "W", "D", "W"],
        "descanso_ganando": 0.65,
        "historial": [
            # Semis vuelta vs Pachuca    (Local)      1-0 | Jordan Carrillo | avanza por pos.
            ["W", 1, 0, 1],
            # Semis ida   vs Pachuca    (Visitante)  0-1 derrota | Idrissi
            ["L", 0, 1, 0],
            # Cuartos vuelta vs América  (Local)      3-3 | avanza por pos. (global 6-6)
            ["D", 3, 3, 1],
            # Cuartos ida   vs América  (Visitante)  3-3 Clásico Capitalino
            ["D", 3, 3, 0],
            ["W", 2, 0, 1],  # J17 vs Pachuca      (Local)    arrebata liderato
            ["W", 3, 1, 1],  # J16 vs Juárez       (Local)
            ["W", 2, 0, 0],  # J15 vs Atl.SanLuis  (Visitante)
            ["W", 3, 1, 1],  # J14 vs Mazatlán     (Local)
            ["D", 2, 2, 0],  # J13 vs Chivas       (Visitante)
            ["W", 1, 0, 1],  # J12 vs América      (Local)
        ]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # CRUZ AZUL — 3° tabla | Joel Huiqui DT interino | En busca del 10°
    # Eliminó a Atlas (4-2 global) y Chivas (4-3 global)
    # Ebere + Palavecino en forma | Sin poder usar Estadio Banorte (FIFA/Mundial)
    # Final ida: local en Estadio Cuauhtémoc, Puebla | Vuelta: visitante en CU
    # ─────────────────────────────────────────────────────────────────────────
    "Cruz Azul": {
        "pos": 3, "gf_p": 2.2, "gc_p": 1.1, "posesion": 0.56,
        "tiros_arco": 6.4, "duelos": 0.514,
        "racha": ["W", "D", "W", "W", "W"],
        "descanso_ganando": 0.62,
        "historial": [
            # Semis vuelta vs Chivas     (Visitante)  2-1 | Márquez + Palavecino
            ["W", 2, 1, 0],
            # Semis ida   vs Chivas     (Local)      2-2 | Rodríguez + Ebere (pen)
            ["D", 2, 2, 1],
            # Cuartos vuelta vs Atlas   (Local)      1-0 | clasifica 4-2 global
            ["W", 1, 0, 1],
            # Cuartos ida   vs Atlas    (Visitante)  3-2 | Ebere doblete
            ["W", 3, 2, 0],
            ["W", 4, 1, 1],  # J17 vs Necaxa       (Local)
            ["D", 0, 0, 0],  # J16 vs Querétaro    (Visitante)
            ["D", 1, 1, 1],  # J15 vs Tijuana      (Local)
            ["D", 1, 1, 0],  # J14 vs América      (Visitante)
            ["L", 1, 2, 1],  # J13 vs Pachuca      (Local)
            ["D", 1, 1, 0],  # J12 vs Mazatlán     (Visitante)
        ]
    },

}

# ─────────────────────────────────────────────────────────────────────────────
# FINAL Clausura 2026
# Pumas (1°) vs Cruz Azul (3°)
# Tercera final histórica entre ambos: Cruz Azul ganó 1978-79, Pumas ganó 1980-81
# En final: empate en 180 min → tiempo extra (no aplica criterio de tabla)
#
# Ida:    Jue 21 may 20:00 hrs — Est. Cuauhtémoc, Puebla (Cruz Azul "local")
#         El Estadio Banorte ya está bajo control FIFA para el Mundial 2026
# Vuelta: Dom 24 may 19:15 hrs — Est. Olímpico Universitario, CDMX (Pumas local)
# ─────────────────────────────────────────────────────────────────────────────

jornada = [
    # Jue 21 may 20:00 — Estadio Cuauhtémoc, Puebla (Cruz Azul "local")
    {"local": "Cruz Azul", "visitante": "Pumas"},
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
    print("=" * 65)
    print("  BetDecision — Liguilla Clausura 2026")
    print("  GRAN FINAL — Ida (21 mayo, Estadio Cuauhtémoc, Puebla)")
    print("=" * 65)
    print(f"  Equipos: {len(equipos)}  |  Partido: {len(jornada)}")
    print()

    print("  CAMINO A LA FINAL:")
    camino = [
        ("Pumas",     "Cuartos", "vs América  3-3 (6-6 global, avanza por pos.)"),
        ("Pumas",     "Semis",   "vs Pachuca  1-1 (global, avanza por pos.)"),
        ("Cruz Azul", "Cuartos", "vs Atlas    4-2 global"),
        ("Cruz Azul", "Semis",   "vs Chivas   4-3 global"),
    ]
    for c in camino:
        print(f"    {c[0]:12} {c[1]:8}  {c[2]}")
    print()

    print("  FORMA RECIENTE Y DIFERENCIAL DE GOLES:")
    for partido in jornada:
        l = partido["local"]
        v = partido["visitante"]
        print(f"    {l:14} vs {v:14} | "
              f"Forma L: {get_forma_reciente(l):.2f} "
              f"V: {get_forma_reciente(v):.2f} | "
              f"DifG L: {get_diferencial_goles(l):+.2f} "
              f"V: {get_diferencial_goles(v):+.2f}")
    print()
    print("  NOTA: En la Final no aplica criterio de tabla.")
    print("  Si hay empate en 180 min → tiempo extra.")
    print("=" * 65)
