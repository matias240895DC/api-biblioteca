from typing import Annotated

from fastapi import APIRouter, Query, Response

from config.response import Response as ErrorResponse, ResponseGetById
from config.response import ResponseGet
from datos.datos import Datos
from datos.schemas.schemas import (
    Libro,
    LibroCreate,
    LibroFiltros,
    LibroParametros,
    LibrosPaginados,
)

router = APIRouter(tags=["Biblioteca"])
# Instancia de la clase Datos para usar en el router
datos = Datos()


@router.get("/", summary="Obtener la API de la biblioteca")
def read_root():
    return {"mensaje": "API de la biblioteca"}


@router.post(
    "/libros",
    summary="Crear un nuevo libro",
    response_model=Libro,
    status_code=201,
    description="Crear un nuevo libro",
    responses={
        409: ErrorResponse(detail="El autor y el nombre del libro ya existe").error409(
            detail="El autor y el nombre del libro ya existe",
            description="Ya existe un libro con el mismo título y autor",
        ),
        422: ErrorResponse(detail="Datos inválidos").error422(
            description="Datos inválidos"
        ),
        201: ErrorResponse.post_response(),
    },
)
def crear_libro(libro: LibroCreate) -> Libro:
    return datos.agregar_libro(libro)


@router.get(
    "/libros",
    summary="Obtener todos los libros",
    response_model=LibrosPaginados,
    description="Obtener todos los libros",
    responses={
        422: ResponseGet(detail="Query params inválidos").error422(),
    },
)
def obtener_libros(
    filtros: Annotated[LibroFiltros, Query()],
) -> LibrosPaginados:
    return datos.obtener_libros(filtros)


@router.get(
    "/libros/estadisticas",
    summary="Obtener las estadísticas de los libros",
    response_model=dict[str, int],
    description="Obtener las estadísticas de los libros",
)
def obtener_estadisticas_libros() -> dict[str, int]:
    return datos.estadisticas_libros()


@router.get(
    "/libros/{id}",
    summary="Obtener un libro por su id",
    response_model=Libro,
    description="Obtener un libro por su id",
    responses={
        404: ResponseGetById(detail="El libro no existe").error404(),
        422: ResponseGetById(detail="Path param 'id' inválido").error422(),
    },
)
def obtener_libro_por_id(id: int) -> Libro:
    return datos.obtener_libro_por_id(id)


@router.delete(
    "/libros/{id}",
    summary="Eliminar un libro por su id",
    status_code=204,
    description="Eliminar un libro por su id",
    responses={
        404: ErrorResponse(detail="El libro no existe").error404(),
        422: ResponseGetById(detail="Path param 'id' inválido").error422(),
    },
)
def eliminar_libro(id: int) -> Response:
    return datos.eliminar_libro(id)


@router.patch(
    "/libros/{id}",
    summary="Actualizar parcialmente un libro por su id",
    response_model=Libro,
    description=(
        "Actualización parcial: solo se modifican los campos enviados. "
        "Un body vacío {} deja el libro igual (200)."
    ),
    responses={
        404: ErrorResponse(detail="El libro no existe").error404(
            detail="El libro no existe",
            description="No hay libro con ese path param 'id'",
        ),
        422: ResponseGetById(detail="Datos inválidos").error422(
            description=(
                "Path 'id' inválido (no entero o <= 0) "
                "o body con campos de tipo incorrecto"
            ),
        ),
    },
)
def actualizar_libro_parcial(id: int, libro: LibroParametros) -> Libro:
    return datos.actualizar_libro_parcial(id, libro)


@router.put(
    "/libros/{id}",
    summary="Actualizar totalmente un libro por su id",
    response_model=Libro,
    description=(
        "Reemplazo total del libro (titulo, autor, anio; disponible opcional). "
        "Mantiene el mismo id."
    ),
    responses={
        404: ErrorResponse(detail="El libro no existe").error404(
            detail="El libro no existe",
            description="No hay libro con ese path param 'id'",
        ),
        422: ResponseGetById(detail="Datos inválidos").error422(
            description=(
                "Path 'id' inválido o body inválido "
                "(mismas reglas que POST: titulo, autor, anio)"
            ),
        ),
        409: ErrorResponse(detail="El autor y el nombre del libro ya existe").error409(
            detail="El autor y el nombre del libro ya existe",
            description=(
                "Otro libro (id distinto) ya tiene el mismo titulo y autor. "
                "Se compara sin distinguir mayúsculas."
            ),
        ),
    },
)
def actualizar_libro_total(id: int, libro: LibroCreate) -> Libro:
    return datos.actualizar_libro_total(id, libro)


@router.post(
    "/libros/{id}/prestar",
    summary="Prestar un libro por su id",
    response_model=Libro,
    description="Marca el libro como prestado (disponible = false).",
    responses={
        404: ErrorResponse(detail="El libro no existe").error404(
            detail="El libro no existe",
            description="No hay libro con ese path param 'id'",
        ),
        422: ResponseGetById(detail="id inválido").error422(
            description="Path key 'id' inválido (no entero o <= 0)",
        ),
        409: ErrorResponse(detail="El libro no está disponible").error409(
            detail="El libro con el titulo: ... no está disponible",
            description="Conflicto: el libro ya estaba prestado (disponible = false)",
        ),
    },
)
def prestar_libro(id: int) -> Libro:
    return datos.prestar_libro(id)


@router.post(
    "/libros/{id}/devolver",
    summary="Devolver un libro por su id",
    response_model=Libro,
    description="Marca el libro como disponible (disponible = true).",
    responses={
        404: ErrorResponse(detail="El libro no existe").error404(
            detail="El libro no existe",
            description="No hay libro con ese path param 'id'",
        ),
        422: ResponseGetById(detail="id inválido").error422(
            description="Path key 'id' inválido (no entero o <= 0)",
        ),
        409: ErrorResponse(detail="El libro ya está disponible").error409(
            detail="El libro con el titulo: ... ya está disponible",
            description="Conflicto: el libro ya estaba disponible (disponible = true)",
        ),
    },
)
def devolver_libro(id: int) -> Libro:
    return datos.devolver_libro(id)
