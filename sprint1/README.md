# BetDecision — Sprint 1
**CompuPapus · IL355 Análisis de Algoritmos · CUCEI UdG · NRC 204835 · 2026-A**

Sistema de recomendaciones de apuestas deportivas para Liga MX basado en regresión lineal y algoritmos Knapsack 0/1.

---

## Contenido del Sprint 1

```
sprint1/
├── backend/
│   ├── datos_equipos.py   ← Historial 18 equipos + jornada 15 hardcodeada
│   ├── regresion.py       ← Cálculo de momios objetivos (regresión lineal)
│   ├── database.py        ← Conexión MySQL + login/registro (tabla usuarios)
│   └── main.py            ← FastAPI: /registro  /login  /partidos
└── frontend/
    ├── login.html         ← Formulario login/registro (UI provisional)
    └── pantalla1.html     ← Lista de partidos con EV (UI provisional)
```

> **Nota:** La UI visual final (dark theme, fuentes Orbitron/Bebas Neue, tarjetas con gradientes) se completa en Sprint 3. En este sprint el frontend es funcional pero sin estilos finales.

---

## Requisitos

- Python 3.10 o superior
- MySQL corriendo localmente (Laragon o XAMPP)
- Paquetes Python:

```bash
pip install fastapi uvicorn mysql-connector-python
```

---

## Configuración de MySQL

Antes de arrancar el servidor, abre `backend/database.py` y ajusta la contraseña de tu MySQL local:

```python
CONFIG_SIN_DB = {
    "host":     "localhost",
    "user":     "root",
    "password": "",   # ← tu contraseña aquí
}

CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",   # ← tu contraseña aquí
    "database": "betdecision"
}
```

La base de datos `betdecision` y la tabla `usuarios` se crean automáticamente al iniciar el servidor si no existen.

---

## Cómo ejecutar

Desde la carpeta `backend/`:

```bash
uvicorn main:app --reload
```

El servidor queda disponible en `http://localhost:8000`.

---

## Cómo probar — Sprint 1

En este sprint **la forma recomendada de probar es mediante Swagger UI**, ya que los HTML del frontend hacen `fetch()` al puerto 8000 y no funcionan si se abren como archivo local.

### Swagger UI (recomendado)

Abre en el navegador:
```
http://localhost:8000/docs
```

Rutas disponibles en Sprint 1:

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/registro` | Crear cuenta nueva |
| `POST` | `/login` | Iniciar sesión |
| `GET` | `/partidos` | Momios objetivos de la Jornada 15 |
| `GET` | `/` | Página de login (HTML) |
| `GET` | `/partidos-page` | Pantalla 1 (HTML) |

Las rutas `/calcular`, `/guardar`, `/historial` y `/acierto` devuelven `HTTP 501 - Pendiente` hasta sus sprints correspondientes.

### Ejemplo: registrar usuario

En Swagger, `POST /registro` → `Try it out`:
```json
{
  "nombre": "Axel Gómez",
  "correo": "axel@compupapus.com",
  "password": "123456"
}
```

### Ejemplo: login

`POST /login` → `Try it out`:
```json
{
  "correo": "axel@compupapus.com",
  "password": "123456"
}
```

### Ejemplo: ver partidos de la jornada

`GET /partidos` → `Try it out` → `Execute`.

Devuelve los 9 partidos de la Jornada 15 ordenados de mayor a menor EV, con momios objetivos calculados por regresión lineal. Cada partido incluye:
- Momio y probabilidad para local, empate y visitante
- Resultado recomendado (mayor EV)
- Bandera `ev_positivo` (candidatos al Knapsack en Sprint 2)

---

## Verificar los módulos por separado

```bash
# Verificar datos de equipos
python datos_equipos.py

# Verificar cálculo de momios (imprime tabla con sumas de probabilidades)
python regresion.py

# Verificar conexión a MySQL y operaciones de usuario
python database.py
```

---

## Cambios en main.py respecto a la versión anterior

| Problema | Solución aplicada |
|----------|-------------------|
| `on_event("startup")` deprecado en FastAPI moderno | Reemplazado por patrón `lifespan` con `@asynccontextmanager` |
| `RuntimeError` si la carpeta `frontend/static/` no existe | Guard `if os.path.isdir(STATIC_DIR)` — el servidor arranca de todas formas e imprime un aviso |
| `os.path.dirname(__file__)` devuelve cadena vacía al ejecutar desde el mismo directorio en Windows | Cambiado a `os.path.abspath(__file__)` para resolver siempre la ruta absoluta correcta |

---

## Historias de usuario completadas

- **H1 completa** — Login y registro de usuario con MySQL
- **H2 inicio** — Regresión lineal calculando momios objetivos; partidos ordenados por EV via `/partidos`

## Pendiente para Sprint 2

- Implementar los 3 algoritmos Knapsack: Fuerza Bruta O(2ⁿ), Programación Dinámica O(n×C), Greedy O(n log n)
- Ruta `POST /calcular` con comparativa de tiempos de ejecución
- UI final de Pantalla 1 (dark theme completo)
- Inicio de Pantalla 2 (input capital + visualización de resultados)

---

## Equipo

| Integrante | # | Rol |
|---|---|---|
| David Yoel Aguilar Urenda | 224003035 | Product Owner |
| Héctor Axel Gómez Franco | 220418303 | Scrum Master |
| Diana Sarahí Vázquez Medina | 220419954 | Product Owner |
| Luis Eduardo Huitrado Márquez | 218552949 | Scrum Master |

Repositorio: https://github.com/JustNoel05/CompuPapus
