# ─────────────────────────────────────────────────────────────────────────────
# huffman.py — CompuPapus / BetDecision
# Algoritmo de Huffman para compresión del reporte de historial
# Complejidad: O(n log n) — donde n = número de símbolos únicos
# Uso: genera un archivo .txt comprimido descargable desde Pantalla 3
# ─────────────────────────────────────────────────────────────────────────────

import heapq
from collections import Counter


# ─────────────────────────────────────────────────────────────────────────────
# NODO DEL ÁRBOL DE HUFFMAN
# Cada nodo almacena un símbolo (carácter) y su frecuencia.
# Los nodos internos tienen frecuencia = suma de sus hijos.
# ─────────────────────────────────────────────────────────────────────────────

class NodoHuffman:
    """
    Nodo del árbol binario de Huffman.

    Atributos:
        simbolo   → carácter representado (None en nodos internos)
        frecuencia→ número de apariciones en el texto
        izquierda → hijo izquierdo (bit 0)
        derecha   → hijo derecho  (bit 1)
    """

    def __init__(self, simbolo, frecuencia):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    # heapq necesita poder comparar nodos entre sí
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

    def __eq__(self, otro):
        return self.frecuencia == otro.frecuencia


# ─────────────────────────────────────────────────────────────────────────────
# CONSTRUCCIÓN DEL ÁRBOL  O(n log n)
# ─────────────────────────────────────────────────────────────────────────────

def construir_arbol(texto):
    """
    Construye el árbol de Huffman a partir de un texto.

    Pasos:
        1. Contar frecuencias de cada carácter  → O(n)
        2. Crear un min-heap con los nodos hoja → O(n log n)
        3. Mientras queden ≥2 nodos en el heap:
           - Extraer los dos de menor frecuencia
           - Crear nodo interno con suma de frecuencias
           - Insertar de vuelta al heap
        4. La raíz del árbol es el único nodo restante

    Retorna:
        (raiz, frecuencias) — raíz del árbol y dict de frecuencias
    """
    if not texto:
        return None, {}

    # Paso 1 — contar frecuencias
    frecuencias = Counter(texto)

    # Caso especial: texto con un solo símbolo único
    if len(frecuencias) == 1:
        simbolo = list(frecuencias.keys())[0]
        raiz = NodoHuffman(simbolo, frecuencias[simbolo])
        return raiz, frecuencias

    # Paso 2 — crear heap inicial con nodos hoja
    heap = [NodoHuffman(simbolo, freq)
            for simbolo, freq in frecuencias.items()]
    heapq.heapify(heap)   # O(n)

    # Paso 3 — construir el árbol fusionando nodos  O(n log n)
    while len(heap) > 1:
        izquierda = heapq.heappop(heap)   # menor frecuencia
        derecha = heapq.heappop(heap)   # segunda menor

        # Nodo interno: no tiene símbolo propio
        nodo_interno = NodoHuffman(
            None, izquierda.frecuencia + derecha.frecuencia)
        nodo_interno.izquierda = izquierda
        nodo_interno.derecha = derecha

        heapq.heappush(heap, nodo_interno)

    return heap[0], frecuencias


# ─────────────────────────────────────────────────────────────────────────────
# GENERACIÓN DE CÓDIGOS  O(n)
# Recorre el árbol y asigna código binario a cada símbolo
# ─────────────────────────────────────────────────────────────────────────────

def generar_codigos(raiz):
    """
    Recorre el árbol de Huffman y genera el código binario de cada símbolo.

    Convenio:
        Rama izquierda → bit '0'
        Rama derecha   → bit '1'

    Retorna:
        dict {simbolo: codigo_binario_str}
    """
    codigos = {}

    def _recorrer(nodo, codigo_actual):
        if nodo is None:
            return

        # Nodo hoja: guardar el código acumulado
        if nodo.simbolo is not None:
            # Caso borde: árbol de un solo nodo
            codigos[nodo.simbolo] = codigo_actual if codigo_actual else "0"
            return

        _recorrer(nodo.izquierda, codigo_actual + "0")
        _recorrer(nodo.derecha,   codigo_actual + "1")

    _recorrer(raiz, "")
    return codigos


# ─────────────────────────────────────────────────────────────────────────────
# CODIFICACIÓN  O(n)
# Convierte el texto original en una cadena de bits usando los códigos
# ─────────────────────────────────────────────────────────────────────────────

def codificar(texto, codigos):
    """
    Transforma el texto en su representación binaria comprimida.

    Retorna:
        str — cadena de '0' y '1' que representa el texto codificado
    """
    return "".join(codigos[caracter] for caracter in texto)


# ─────────────────────────────────────────────────────────────────────────────
# DECODIFICACIÓN  O(n)
# Recorre el árbol siguiendo los bits para reconstruir el texto original
# ─────────────────────────────────────────────────────────────────────────────

def decodificar(bits, raiz):
    """
    Reconstruye el texto original a partir de la cadena de bits y el árbol.

    Recorre el árbol bit a bit:
        '0' → ir a hijo izquierdo
        '1' → ir a hijo derecho
    Al llegar a una hoja, emite el símbolo y vuelve a la raíz.

    Retorna:
        str — texto decodificado
    """
    if raiz is None:
        return ""

    # Caso borde: árbol de un solo símbolo
    if raiz.simbolo is not None:
        return raiz.simbolo * len(bits)

    resultado = []
    nodo_actual = raiz

    for bit in bits:
        nodo_actual = nodo_actual.izquierda if bit == "0" else nodo_actual.derecha

        if nodo_actual.simbolo is not None:
            resultado.append(nodo_actual.simbolo)
            nodo_actual = raiz   # volver a la raíz para el siguiente símbolo

    return "".join(resultado)


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL — comprimir_historial
# Punto de entrada desde main.py
# ─────────────────────────────────────────────────────────────────────────────

def comprimir_historial(texto):
    """
    Aplica el algoritmo de Huffman al texto del reporte de historial.

    Proceso completo:
        1. Construir árbol de Huffman a partir del texto
        2. Generar tabla de códigos binarios
        3. Codificar el texto
        4. Calcular métricas de compresión

    Parámetros:
        texto → str con el contenido completo del reporte

    Retorna dict con:
        texto_original     → str
        bits_codificados   → str (cadena de 0s y 1s)
        codigos            → dict {char: codigo}
        frecuencias        → dict {char: count}
        bits_originales    → int (tamaño sin comprimir en bits, ASCII = 8 bits/char)
        bits_comprimidos   → int (tamaño codificado en bits)
        tasa_compresion    → float (porcentaje de reducción)
        simbolos_unicos    → int
        complejidad        → str
    """
    raiz, frecuencias = construir_arbol(texto)

    if raiz is None:
        return None

    codigos = generar_codigos(raiz)
    bits_codificados = codificar(texto, codigos)

    bits_originales = len(texto) * 8          # ASCII: 8 bits por carácter
    bits_comprimidos = len(bits_codificados)
    n_simbolos = len(frecuencias)

    tasa = round((1 - bits_comprimidos / bits_originales)
                 * 100, 2) if bits_originales > 0 else 0

    return {
        "texto_original":   texto,
        "bits_codificados": bits_codificados,
        "codigos":          codigos,
        "frecuencias":      frecuencias,
        "bits_originales":  bits_originales,
        "bits_comprimidos": bits_comprimidos,
        "tasa_compresion":  tasa,
        "simbolos_unicos":  n_simbolos,
        "complejidad":      f"O({n_simbolos} log {n_simbolos})",
    }


# ─────────────────────────────────────────────────────────────────────────────
# GENERADOR DE REPORTE — formato texto plano del historial
# ─────────────────────────────────────────────────────────────────────────────

def generar_texto_reporte(historial, usuario_nombre, pct_aciertos):
    """
    Convierte el historial del usuario a texto plano estructurado.
    Este texto es el que se comprime con Huffman.

    Mientras más jornadas tenga el usuario, mayor será el texto
    y más significativa la compresión — justificación académica del algoritmo.

    Parámetros:
        historial       → lista de sugerencias (de database.get_historial)
        usuario_nombre  → nombre del usuario autenticado
        pct_aciertos    → porcentaje global de aciertos (float o None)

    Retorna:
        str — reporte completo en texto plano
    """
    lineas = []
    sep = "=" * 60

    lineas.append(sep)
    lineas.append("  BETDECISION — Reporte de Historial de Apuestas")
    lineas.append("  Liga MX | Clausura 2026 | Análisis de Algoritmos")
    lineas.append("  CompuPapus — CUCEI UdG — IL355")
    lineas.append(sep)
    lineas.append(f"  Usuario : {usuario_nombre}")
    lineas.append(f"  Jornadas: {len(historial)}")
    lineas.append(
        f"  Aciertos: {pct_aciertos}%" if pct_aciertos is not None else "  Aciertos: Sin datos aún")
    lineas.append(sep)

    for sug in historial:
        lineas.append("")
        lineas.append(
            f"  [{sug.get('fecha', '—')}]  {sug.get('jornada', '—')}")
        lineas.append(f"  Capital: ${sug.get('capital', 0):.2f}   "
                      f"Ganancia estimada: +${sug.get('ganancia_est', 0):.2f}")
        lineas.append("  " + "-" * 56)

        for p in sug.get("partidos", []):
            estado = "✓ ACERTÓ" if p.get("acerto") == 1 else \
                     "✗ FALLÓ " if p.get("acerto") == 0 else \
                     "? PENDIENTE"
            lineas.append(
                f"  {estado}  {p.get('partido', '—')[:30]:<30}  "
                f"${p.get('apuesta', 0):.0f}"
            )

        # Resumen de la sugerencia
        partidos_marcados = [p for p in sug.get(
            "partidos", []) if p.get("acerto") is not None]
        if partidos_marcados:
            aciertos = sum(
                1 for p in partidos_marcados if p.get("acerto") == 1)
            lineas.append(
                f"  Resultado: {aciertos}/{len(partidos_marcados)} acertados")

    lineas.append("")
    lineas.append(sep)
    lineas.append("  Reporte generado con compresión Huffman O(n log n)")
    lineas.append("  BetDecision v2 — CompuPapus 2026")
    lineas.append(sep)

    return "\n".join(lineas)


# ─────────────────────────────────────────────────────────────────────────────
# PRUEBA — correr directamente para verificar el algoritmo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    texto_prueba = (
        "BetDecision Reporte Historial Liga MX Clausura 2026 "
        "Pumas vs America Cruz Azul vs Atlas Pachuca vs Toluca "
        "Guadalajara vs Tigres Capital 500 Ganancia estimada "
        "acerto fallo pendiente recomendacion algoritmo Huffman "
    ) * 5   # repetir para que la compresión sea más evidente

    print("=" * 60)
    print("  HUFFMAN — Prueba de compresión")
    print("=" * 60)

    resultado = comprimir_historial(texto_prueba)

    print(f"\n  Texto original:    {len(texto_prueba)} caracteres")
    print(f"  Símbolos únicos:   {resultado['simbolos_unicos']}")
    print(f"  Complejidad:       {resultado['complejidad']}")
    print(f"\n  Bits sin comprimir: {resultado['bits_originales']}")
    print(f"  Bits comprimidos:   {resultado['bits_comprimidos']}")
    print(f"  Tasa de compresión: {resultado['tasa_compresion']}%")

    print(f"\n  Tabla de códigos (top 10 por frecuencia):")
    top = sorted(resultado["frecuencias"].items(), key=lambda x: -x[1])[:10]
    for simbolo, freq in top:
        codigo = resultado["codigos"][simbolo]
        nombre = repr(simbolo)
        print(f"    {nombre:6} → {codigo:15} (freq: {freq}, bits: {len(codigo)})")

    # Verificar que la decodificación es correcta
    raiz_verificacion, _ = construir_arbol(texto_prueba)
    decodificado = decodificar(
        resultado["bits_codificados"], raiz_verificacion)
    print(f"\n  Verificación (decodificación correcta): "
          f"{'✓ OK' if decodificado == texto_prueba else '✗ ERROR'}")
    print("=" * 60)
