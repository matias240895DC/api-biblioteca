# API Biblioteca

API REST de una biblioteca con **FastAPI**, **Uvicorn** y **Pydantic**.

Los libros viven en memoria y se **persisten** en `datos/libros.json` (pathlib; carga al iniciar, guarda tras cada cambio). Hay **logging** (sin `print`) y el código pasa `ruff check`.

- Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## Estructura del proyecto

```text
api-biblioteca/
├── main.py                 # App, logging, handler 422 en español
├── ruff.toml               # Config de Ruff (ignore TRY004, exclude venv)
├── requirements.txt
├── readme.md
├── .gitignore
├── datos/
│   ├── __init__.py
│   ├── datos.py            # Lógica + cargar/guardar JSON
│   ├── libros.json         # Persistencia (lista de libros)
│   └── schemas/
│       ├── schemas.py      # Create, Libro, Filtros, Parametros, Paginados
│       └── error.py        # Examples de errores para Swagger
└── routers/
    ├── __init__.py
    └── libros.py           # Endpoints HTTP
```

| Archivo | Rol |
|---------|-----|
| `main.py` | App, logging, router, errores 422 |
| `ruff.toml` | Reglas de lint (Ruff) |
| `routers/libros.py` | Endpoints |
| `datos/datos.py` | CRUD, filtros, prestar/devolver, JSON |
| `datos/libros.json` | Datos en disco |
| `datos/schemas/schemas.py` | Validación Pydantic |
| `datos/schemas/error.py` | Docs 404/409/422 en `/docs` |

---

## Requisitos

Antes de empezar, asegurate de tener instalado:

- **Python 3.10 o superior**
- **pip** (normalmente viene con Python)

Para comprobarlo, abrí una terminal e ingresá:

```bash
python --version
```

En **macOS / Linux**, si no reconoce `python`, ingresá:

```bash
python3 --version
```

Deberías ver algo como `Python 3.11.x` o superior.

---

## Instalación y ejecución

Seguí estos pasos **en orden**. Todos los comandos se escriben en la terminal y se confirman con Enter.

### Paso 0 — Abrir la terminal

| Sistema | Cómo |
|---------|------|
| **Windows** | Abrí **PowerShell**, **CMD**, o la terminal de tu IDE de preferencia |
| **macOS** | Abrí **Terminal**, o la terminal de tu IDE de preferencia |
| **Linux** | Abrí tu terminal (Ctrl+Alt+T en muchas distros), o la de tu IDE de preferencia |

### Paso 1 — Ir a la carpeta del proyecto

En la terminal, ingresá el comando `cd` hasta llegar a la carpeta `api-biblioteca` (donde está el archivo `main.py`).

Ejemplo (adaptá la ruta a tu máquina):

**Windows:**

```powershell
cd C:\Users\Matias\Desktop\Backend-python\api-biblioteca
```

**macOS / Linux:**

```bash
cd ~/Desktop/Backend-python/api-biblioteca
```

Para verificar que estás en el lugar correcto, ingresá:

```bash
dir
```

En macOS / Linux:

```bash
ls
```

Tenés que ver `main.py`, `requirements.txt` y las carpetas `datos` y `routers`.

### Paso 2 — Crear el entorno virtual

En la terminal, ingresá:

**Windows:**

```powershell
python -m venv venv
```

**macOS / Linux:**

```bash
python3 -m venv venv
```

Esto crea una carpeta `venv` dentro del proyecto. No la subas a Git (va en `.gitignore`).

### Paso 3 — Activar el entorno virtual

En la terminal, ingresá:

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

Si aparece un error de política de ejecución, ingresá primero:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

y volvé a intentar el `Activate.ps1`.

**Windows (CMD):**

```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

Si salió bien, al inicio del prompt deberías ver `(venv)`.

### Paso 4 — Instalar las dependencias

Con el venv **activado**, en la terminal ingresá:

```bash
pip install -r requirements.txt
```

Esperá a que termine. Eso instala FastAPI, Uvicorn, Pydantic y **Ruff** (el linter que pide la consigna).

### Paso 5 — Levantar la API

Con el venv activo y estando dentro de `api-biblioteca`, en la terminal ingresá:

```bash
uvicorn main:app --reload
```

Si arrancó bien, vas a ver mensajes de Uvicorn y los logs de inicio. Dejá esa terminal abierta mientras usás la API.

Abrí el navegador e ingresá a:

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Documentación Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

**Importante:** siempre ejecutá `uvicorn` desde la carpeta `api-biblioteca`, con el venv activo, y sin otro proceso ocupando el puerto **8000**.

### Paso 6 — Detener el servidor

Volvé a la terminal donde corre uvicorn y presioná `Ctrl+C` (a veces hace falta dos veces por `--reload`).

### Paso 7 — Salir del entorno virtual (opcional)

En la terminal, ingresá:

```bash
deactivate
```

### Comprobaciones rápidas

Con el venv activo y el servidor **apagado**, en la terminal ingresá:

```bash
python -c "import main"
```

No debe imprimir nada.

Para el linter, ingresá:

```bash
ruff check .
```

Debería responder: `All checks passed!`.

### Resumen rápido de comandos

| Paso | Windows (PowerShell) | macOS / Linux |
|------|----------------------|---------------|
| Ir al proyecto | `cd ruta\api-biblioteca` | `cd ruta/api-biblioteca` |
| Crear venv | `python -m venv venv` | `python3 -m venv venv` |
| Activar | `.\venv\Scripts\Activate.ps1` | `source venv/bin/activate` |
| Instalar | `pip install -r requirements.txt` | igual |
| Correr | `uvicorn main:app --reload` | igual |
| Detener | `Ctrl+C` | `Ctrl+C` |
| Salir del venv | `deactivate` | `deactivate` |

---

## Problemas frecuentes (cómo afrontarlos)

### 1) Instalé los paquetes en el Python global (sin venv)

**Síntoma:** instalaste `fastapi` / `uvicorn` **antes** de activar el venv, o sin ver `(venv)` en el prompt. Quedaron en el Python de todo el sistema.

**Cómo comprobarlo**

| Pregunta | Comando |
|----------|---------|
| ¿Estoy en el venv? | Tiene que verse `(venv)` al inicio del prompt |
| ¿Qué hay en el **global**? | Windows: `py -m pip list` · macOS/Linux: `python3 -m pip list` (sin venv) |
| ¿Qué hay en el **venv**? | Con `(venv)` activo: `pip list` |

**Solución**

1. Desinstalá del Python **global** (no del venv).

**Windows** (sin `(venv)` en el prompt, o después de `deactivate`):

```powershell
py -m pip uninstall fastapi uvicorn starlette pydantic pydantic-core anyio annotated-doc annotated-types typing-inspection opentelemetry-api click h11 idna typing-extensions ruff -y
```

**macOS / Linux:**

```bash
deactivate
python3 -m pip uninstall fastapi uvicorn starlette pydantic pydantic-core anyio annotated-doc annotated-types typing-inspection opentelemetry-api click h11 idna typing-extensions ruff -y
```

- `py -m pip` / `python3 -m pip` → pip del Python **global**
- `-y` → confirma el sí automáticamente

2. Activá el venv e instalá **dentro** del proyecto:

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
```

**Flujo correcto la próxima vez:** crear venv → activar (ver `(venv)`) → recién ahí `pip install ...`.

---

### 2) El puerto 8000 está ocupado / la API se “cuelga”

**Síntoma:** al correr `uvicorn main:app --reload` aparece `Address already in use`, `error while attempting to bind`, o el servidor viejo sigue respondiendo aunque “cerraste” la terminal. Suele ser por **varias instancias** de uvicorn en el puerto **8000**.

**Solución A — Cortar bien la instancia actual**

1. Hacé clic en la terminal donde corre uvicorn.
2. Presioná `Ctrl+C` (a veces **dos veces** por `--reload`).
3. Esperá a que diga que el proceso terminó.
4. Volvé a levantar: `uvicorn main:app --reload`.

**Solución B — Matar lo que usa el puerto 8000 (Windows PowerShell)**

Ingresá en la terminal:

```powershell
netstat -ano | findstr :8000
```

En la última columna aparece el **PID**. Después ingresá (reemplazá `12345` por ese número):

```powershell
taskkill /PID 12345 /F
```

Si hay varias líneas / varios PID, repetí `taskkill` por cada uno.

**Solución C — macOS / Linux**

```bash
lsof -i :8000
```

Anotá el PID y después:

```bash
kill -9 PID
```

**Tip:** no abras 3 terminales con uvicorn a la vez. Una sola instancia en el puerto 8000.

---

### 3) PowerShell no deja activar el venv

**Síntoma:** `cannot be loaded because running scripts is disabled` al hacer `.\venv\Scripts\Activate.ps1`.

**Solución** — ingresá en PowerShell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Después volvé a activar:

```powershell
.\venv\Scripts\Activate.ps1
```

---

### 4) `ModuleNotFoundError: No module named 'fastapi'` (u otro paquete)

**Causa habitual:** el venv no está activo, o nunca corriste `pip install -r requirements.txt` **dentro** del venv.

**Solución**

1. Activá el venv (tiene que verse `(venv)`).
2. Ingresá: `pip install -r requirements.txt`
3. Probá de nuevo: `uvicorn main:app --reload`

---

### 5) `uvicorn` no se reconoce como comando

**Causa:** paquetes no instalados en el venv activo, o venv desactivado.

**Solución:** activá el venv e instalá dependencias otra vez. Alternativa sin depender del PATH:

```bash
python -m uvicorn main:app --reload
```

---

### 6) Estoy en la carpeta equivocada

**Síntoma:** `Could not import module "main"` o no encuentra `requirements.txt`.

**Solución:** en la terminal, `cd` hasta `api-biblioteca` (donde está `main.py`). Verificá con `dir` (Windows) o `ls` (macOS/Linux).

---

### Tabla rápida

| Problema | Qué hacer |
|----------|-----------|
| Paquetes en el global | Desinstalar con `py -m pip` / `python3 -m pip`, activar venv, `pip install -r requirements.txt` |
| Puerto 8000 ocupado | `Ctrl+C`; si sigue, matar el PID del puerto |
| Varias terminales con uvicorn | Dejar **una** sola |
| No activa el venv (PowerShell) | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Falta un módulo | `(venv)` + `pip install -r requirements.txt` |
| No encuentra `main` | `cd` a la carpeta del proyecto |

---

## Persistencia (`datos/libros.json`)

| Momento | Qué pasa |
|---------|----------|
| Arranque | `cargar_libros()` lee el JSON |
| Crear / PUT / PATCH / DELETE / prestar / devolver | `guardar()` reescribe todo el archivo |
| Archivo inexistente, vacío o dañado | API arranca con lista vacía (no crashea) |
| Tras reiniciar | `id_siguiente` = max(id) del archivo |

Ruta con pathlib (no depende de desde dónde ejecutes uvicorn):

```python
Path(__file__).resolve().parent / "libros.json"
```

Formato:

```json
[
  {
    "id": 1,
    "titulo": "rayuela",
    "autor": "julio cortazar",
    "anio": 1963,
    "disponible": true
  }
]
```

`guardar()` no edita una línea: toma `self.libros` completo y pisa el archivo.

---

## Logging

En `main.py`:

```python
logging.basicConfig(level=logging.INFO, format="...")
logger = logging.getLogger(__name__)
```

| Llamada | Cuándo se ve |
|---------|----------------|
| `logger.info("Router de libros registrado")` | Al arrancar / reload |
| `logger.info("API Biblioteca lista")` | Al arrancar / reload |
| `logger.warning("Error de validación...")` | Cuando hay **422** |

No se usa `print`. Un POST **exitoso** no genera log extra (solo arranque y errores 422).

---

## Ruff (lint)

### Cómo ejecutarlo

```powershell
ruff check .
```

(`ruff.toml` ya excluye `venv`.)

### `ruff.toml`

```toml
exclude = ["venv"]

[lint]
ignore = ["TRY004"]
```

### Por qué se ignora `TRY004`

Ruff sugiere `TypeError` cuando el tipo es inválido. En **validators de Pydantic** hay que usar `ValueError`: Pydantic lo convierte en **422**. Si usás `TypeError`, la API responde **500**.

Por eso se deja `ValueError` y se ignora `TRY004`.

### Imports (`I001`)

Ruff pide grupos separados por **una** línea en blanco:

1. stdlib (`typing`)
2. terceros (`fastapi`)
3. tu código (`datos...`) — **juntos**, sin líneas vacías entre ellos

Si falla `I001`, casi siempre es una línea en blanco de más o de menos entre imports.

```powershell
ruff check . --fix   # ordena imports automáticamente
```

---

## Modelos (schemas)

```text
LibroCreate       → body POST / PUT
Libro             → respuesta (+ id)
LibroParametros   → body PATCH (campos opcionales)
LibroFiltros      → query GET (+ desde, limite)  [hereda Parametros]
LibrosPaginados   → respuesta del listado
```

`extra="forbid"` → key desconocida → **422** (`Key inválida: '...'`).

En filtros/búsquedas se usa `is not None` antes de `.lower()` porque título/autor pueden tiparse como opcionales.

---

## Rutas

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Bienvenida |
| `POST` | `/libros` | Crear (**201**) |
| `GET` | `/libros` | Listar (filtros + paginación) |
| `GET` | `/libros/estadisticas` | Totales / disponibles / prestados |
| `GET` | `/libros/{id}` | Por id |
| `PUT` | `/libros/{id}` | Reemplazo total |
| `PATCH` | `/libros/{id}` | Parcial |
| `DELETE` | `/libros/{id}` | Eliminar (**204**) |
| `POST` | `/libros/{id}/prestar` | `disponible = false` |
| `POST` | `/libros/{id}/devolver` | `disponible = true` |

`/libros/estadisticas` va **antes** que `/libros/{id}`; si no, FastAPI toma `"estadisticas"` como id → 422.

Base: `http://127.0.0.1:8000`

---

## POST `/libros` — Crear

```json
{
  "titulo": "Rayuela",
  "autor": "Julio Cortázar",
  "anio": 1963
}
```

| Caso | Código |
|------|--------|
| OK | **201** (id secuencial, `disponible=true`, minúsculas) |
| Mismo título **y** autor | **409** |
| Validación / JSON / key extra | **422** |

---

## GET `/libros` — Filtros + paginación

```text
GET /libros?titulo=rayuela&disponible=true&limite=10&desde=0
```

| Param | Default | Notas |
|-------|---------|--------|
| `titulo` / `autor` / `anio` / `disponible` | — | Opcionales |
| `limite` | `100` | 1–100 |
| `desde` | `0` | ≥ 0 |

Orden: **filtrar → paginar**. Respuesta: `data`, `limite`, `desde`, `total`.

---

## GET `/libros/estadisticas`

```json
{
  "total_libros": 2,
  "total_libros_disponibles": 1,
  "total_libros_prestados": 1
}
```

---

## GET / PUT / PATCH / DELETE `/libros/{id}`

| Método | Comportamiento |
|--------|----------------|
| GET | **200** / **404** / **422** (id ≤ 0) |
| PUT | Reemplazo con `LibroCreate`; mismo id; **409** si choca título+autor |
| PATCH | Solo campos enviados; `{}` → 200 sin cambios |
| DELETE | **204**; también se actualiza el JSON |

---

## Prestar / devolver

| Ruta | Efecto | **409** |
|------|--------|---------|
| `.../prestar` | `disponible=false` | ya prestado |
| `.../devolver` | `disponible=true` | ya disponible |

**200** + libro, **404** si no existe; se guarda en JSON.

---

## Errores 422 en español

Handler en `main.py`: quita `"Value error, "`, traduce mensajes típicos de Pydantic y keys extra.

```json
{ "detail": ["El titulo es obligatorio"] }
```

```json
{ "detail": ["Key inválida: 'autori'"] }
```

---

## Códigos HTTP

| Código | Cuándo |
|--------|--------|
| **200** | GET / PUT / PATCH / prestar / devolver / estadísticas |
| **201** | Creado |
| **204** | DELETE |
| **404** | No existe |
| **409** | Conflicto (duplicado, prestar/devolver) |
| **422** | Validación / id inválido / key extra / JSON inválido |
| **500** | Evitar: no uses `TypeError` en validators de Pydantic |

---

## Checklist de prueba

1. `uvicorn main:app --reload` → ver 2 logs INFO de arranque
2. POST libro → 201 + aparece en `libros.json`
3. Reiniciar → GET `/libros` mantiene datos
4. POST otro → id = max + 1
5. DELETE → sale del JSON
6. GET `/libros/estadisticas`
7. prestar / devolver
8. Body sin título → **422** (no 500) + log WARNING
9. `ruff check .` → `All checks passed!`

---

## Estado consignas de calidad

| Ítem | Estado |
|------|--------|
| Persistencia JSON | Hecho |
| Logging (≥ 3 llamadas, sin print) | Hecho (`main.py`) |
| `ruff check` limpio | Hecho (`ruff.toml` + imports) |
| `summary` o docstring en todos los endpoints | Pendiente (hoy hay `description`) |
