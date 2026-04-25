# ─────────────────────────────────────────────────────────────────────────────
# algoritmos.py — CompuPapus / BetDecision
# Implementación de los 3 algoritmos Knapsack 0/1
# Entrada: lista de partidos con EV positivo + capital del usuario
# Salida:  distribución óptima del capital entre los partidos seleccionados
# ─────────────────────────────────────────────────────────────────────────────

import time
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from regresion import calcular_momios


# ─────────────────────────────────────────────────────────────────────────────
# PREPARACIÓN DE DATOS
# Convierte los partidos de regresion.py al formato que necesita el Knapsack:
# cada partido tiene un "peso" (apuesta) y un "valor" (EV)
# ─────────────────────────────────────────────────────────────────────────────

def preparar_items(partidos, capital):
    """
    Divide el capital equitativamente entre los partidos disponibles
    y asigna ese monto como peso (apuesta) de cada item.
    El valor de cada item es su EV multiplicado por el monto apostado.

    Parámetros:
        partidos → lista de partidos con EV positivo de regresion.py
        capital  → dinero disponible del usuario

    Retorna:
        lista de items listos para el Knapsack
    """
    n = len(partidos)
    if n == 0:
        return []

    total_ev = sum(p["recomendado"]["ev"] for p in partidos)

    items = []
    for p in partidos:
        ev = p["recomendado"]["ev"]
        proporcion = ev / total_ev
        apuesta = round(capital * proporcion)

        items.append({
            "partido":   f"{p['local']} vs {p['visitante']}",
            "local":     p["local"],
            "visitante": p["visitante"],
            "resultado": p["recomendado"]["resultado"],
            "momio":     p["recomendado"]["momio"],
            "prob":      p["recomendado"]["prob"],
            "peso":      apuesta,                    # ← proporcional al EV
            "valor":     round(ev * apuesta, 2),
            "ev":        ev,
        })
    return items


# ─────────────────────────────────────────────────────────────────────────────
# ALGORITMO 1 — FUERZA BRUTA  O(2ⁿ)
# Evalúa todas las combinaciones posibles de partidos
# Garantiza la solución exacta pero crece exponencialmente
# ─────────────────────────────────────────────────────────────────────────────

def fuerza_bruta(items, capital):
    """
    Evalúa las 2ⁿ combinaciones posibles.
    Con n=6 partidos → 2⁶ = 64 combinaciones.

    Retorna la combinación que maximiza la ganancia
    sin exceder el capital disponible.
    """
    inicio = time.perf_counter()
    n = len(items)
    mejor_valor = 0
    mejor_combo = []
    combinaciones_evaluadas = 0

    # Iterar sobre todas las combinaciones posibles (2ⁿ)
    for i in range(1 << n):                        # 1 << n = 2ⁿ
        total_peso = 0
        total_valor = 0
        combo = []
        combinaciones_evaluadas += 1

        for j in range(n):
            if i & (1 << j):                       # si el bit j está activo
                total_peso += items[j]["peso"]
                total_valor += items[j]["valor"]
                combo.append(items[j])

        # Actualizar si esta combinación es mejor y no excede el capital
        if total_peso <= capital and total_valor > mejor_valor:
            mejor_valor = total_valor
            mejor_combo = combo

    tiempoFb = round((time.perf_counter() - inicio)
                     * 1000, 4)  # en milisegundos

    return {
        "algoritmo":    "Fuerza Bruta",
        "complejidad":  f"O(2^{n})",
        "combinaciones": combinaciones_evaluadas,
        "seleccion":    mejor_combo,
        "total_apostado": sum(i["peso"] for i in mejor_combo),
        "ganancia_estimada": round(sum(i["valor"] for i in mejor_combo), 2),
        "tiempo_ms":    tiempoFb,
    }


# ─────────────────────────────────────────────────────────────────────────────
# ALGORITMO 2 — PROGRAMACIÓN DINÁMICA  O(n × C)
# Construye una tabla de subproblemas para encontrar la solución óptima
# Garantiza el óptimo global con eficiencia radicalmente superior
# ─────────────────────────────────────────────────────────────────────────────

def programacion_dinamica(items, capital):
    """
    Construye tabla dp[n+1][C+1] donde:
        dp[i][c] = máxima ganancia usando los primeros i items
                   con un capital de c pesos disponibles

    Retorna la selección óptima reconstruyendo la tabla.
    """
    inicio = time.perf_counter()
    n = len(items)
    C = int(capital)

    # Construir tabla de programación dinámica
    # dp[i][c] → mejor ganancia con i partidos y c pesos de capital
    dp = [[0.0] * (C + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        peso = int(items[i - 1]["peso"])
        valor = items[i - 1]["valor"]

        for c in range(C + 1):
            # Sin incluir el item i
            dp[i][c] = dp[i - 1][c]

            # Incluyendo el item i si cabe en el capital
            if peso <= c:
                con_item = dp[i - 1][c - peso] + valor
                if con_item > dp[i][c]:
                    dp[i][c] = con_item

    # Reconstruir la selección óptima recorriendo la tabla al revés
    seleccion = []
    c = C
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:          # este item fue incluido
            seleccion.append(items[i - 1])
            c -= int(items[i - 1]["peso"])

    tiempoPd = round((time.perf_counter() - inicio) * 1000, 4)

    return {
        "algoritmo":         "Programación Dinámica",
        "complejidad":       f"O({n} × {C})",
        "operaciones":       n * C,
        "seleccion":         seleccion,
        "total_apostado":    sum(i["peso"] for i in seleccion),
        "ganancia_estimada": round(dp[n][C], 2),
        "tiempo_ms":         tiempoPd,
    }


# ─────────────────────────────────────────────────────────────────────────────
# COMPARATIVA — corre los 2 algoritmos y determina el ganador
# ─────────────────────────────────────────────────────────────────────────────

def comparar(partidos_ev_positivo, capital):
    """
    Prepara los items y corre los 2 algoritmos sobre los mismos datos.
    Retorna los resultados de los 2 y determina el algoritmo ganador.
    """
    items = preparar_items(partidos_ev_positivo, capital)

    if not items:
        return None

    fb = fuerza_bruta(items, capital)
    pd = programacion_dinamica(items, capital)

    # El ganador es el que mayor ganancia estimada obtiene
    # En caso de empate, se prefiere el más eficiente (PD)
    ganador = max([fb, pd], key=lambda x: (
        x["ganancia_estimada"], -x["tiempo_ms"]
    ))

    return {
        "fuerza_bruta":          fb,
        "programacion_dinamica": pd,
        "ganador":               ganador["algoritmo"],
        "items":                 items,
    }


# ─────────────────────────────────────────────────────────────────────────────
# PRUEBA — correr directamente para ver resultados
# ─────────────────────────────────────────────────────────────────────────────

# Obtener partidos con EV positivo
todos = calcular_momios()
positivos = [p for p in todos if p["ev_positivo"]]
capital = 500

print("=" * 65)
print(f"  BetDecision — Comparativa de Algoritmos | Capital: ${capital}")
print(f"  Partidos disponibles: {len(positivos)}")
print("=" * 65)

resultado = comparar(positivos, capital)

for nombre, key in [
    ("FUERZA BRUTA",          "fuerza_bruta"),
    ("PROGRAMACIÓN DINÁMICA", "programacion_dinamica"),
]:
    r = resultado[key]
    print(f"\n── {nombre} ──────────────────────────────")
    print(f"   Complejidad:        {r['complejidad']}")
    print(f"   Tiempo:             {r['tiempo_ms']} ms")
    print(f"   Total apostado:     ${r['total_apostado']}")
    print(f"   Ganancia estimada:  ${r['ganancia_estimada']}")
    print(f"   Partidos elegidos:  {len(r['seleccion'])}")
    for item in r["seleccion"]:
        print(f"      → {item['partido']:30} "
              f"{item['resultado']:10} "
              f"momio {item['momio']:.2f}  "
              f"apuesta ${item['peso']}  "
              f"EV {item['ev']:+.2f}")

print(f"\n{'=' * 65}")
print(f" ALGORITMO GANADOR: {resultado['ganador']}")
print(f"{'=' * 65}")


# ─────────────────────────────────────────────
# FUNCIÓN PARA GRAFICAR TIEMPOS REALES
# ─────────────────────────────────────────────

def graficar_tiempos_reales(partidos, capital):
    n_values = []
    fb_times = []
    pd_times = []

    for n in range(1, len(partidos) + 1):
        subset = partidos[:n]
        resultado = comparar(subset, capital)

        n_values.append(n)
        fb_times.append(resultado["fuerza_bruta"]["tiempo_ms"])
        pd_times.append(resultado["programacion_dinamica"]["tiempo_ms"])

    plt.figure()

    plt.plot(n_values, fb_times, marker='o', label="Fuerza Bruta")
    plt.plot(n_values, pd_times, marker='o', label="Programación Dinámica")

    plt.title(f"Tiempos reales vs número de partidos (Capital = {capital})")
    plt.xlabel("Número de partidos (n)")
    plt.ylabel("Tiempo (ms)")

    plt.legend()
    plt.grid()

    plt.show()


# ─────────────────────────────────────────────
# FUNCIÓN DEL BOTÓN
# ─────────────────────────────────────────────

def calcular_y_graficar():
    try:
        capital = int(entry_capital.get())

        todos = calcular_momios()
        positivos = [p for p in todos if p["ev_positivo"]]

        if len(positivos) < 2:
            label_resultado.config(text="No hay suficientes partidos")
            return

        graficar_tiempos_reales(positivos, capital)

    except ValueError:
        label_resultado.config(text="Ingresa un número válido")


if __name__ == "__main__":
    # ─────────────────────────────────────────────
    # GUI
    # ─────────────────────────────────────────────

    ventana = tk.Tk()
    ventana.title("BetDecision - Comparador")
    ventana.geometry("350x200")

    label_titulo = tk.Label(
        ventana,
        text="Ingrese el capital",
        font=("Arial", 12)
    )
    label_titulo.pack(pady=10)

    entry_capital = tk.Entry(ventana, width=25)
    entry_capital.pack(pady=5)

    boton = tk.Button(
        ventana,
        text="Calcular y graficar",
        command=calcular_y_graficar,
        height=2,
        width=25
    )
    boton.pack(pady=15)

    label_resultado = tk.Label(ventana, text="", fg="red")
    label_resultado.pack()

    ventana.mainloop()
