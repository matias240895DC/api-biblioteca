import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers import libros

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="API Biblioteca")
app.include_router(libros.router)


@app.on_event("startup")
async def al_iniciar():
    # Solo al levantar uvicorn, no al hacer `import main`
    logger.info("Router de libros registrado")
    logger.info("API Biblioteca lista")


def mensaje_error(error: dict) -> str:
    msg = str(error.get("msg") or "").replace("Value error, ", "")
    loc = error.get("loc") or ()
    campo = loc[-1] if loc else None

    # extra="forbid" → key/campo que no existe en el schema
    if error.get("type") == "extra_forbidden" or msg == "Extra inputs are not permitted":
        if campo is not None:
            return f"Key inválida: '{campo}'"
        return "Key inválida"

    traducciones = {
        "Field required": "Campo obligatorio",
        "Input should be a valid integer": "Debe ser un número entero",
        "Input should be a valid boolean": "Debe ser true o false",
        "Input should be a valid string": "Debe ser una cadena de texto",
        "JSON decode error": "JSON inválido",
    }
    return traducciones.get(msg, msg)


@app.exception_handler(RequestValidationError)
async def errores_validacion(request: Request, exc: RequestValidationError):
    msgs = [mensaje_error(e) for e in exc.errors()]
    logger.warning("Error de validación en %s: %s", request.url.path, msgs)
    return JSONResponse(status_code=422, content={"detail": msgs})
