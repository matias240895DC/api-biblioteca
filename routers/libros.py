from typing import Annotated

from fastapi import APIRouter, Query, Response

from datos.datos import Datos
from datos.schemas.error import error_responses
from datos.schemas.schemas import (
    Libro,
    LibroCreate,
    LibroFiltros,
    LibroParametros,
    LibrosPaginados,
)

router = APIRouter()
# Instancia de la clase Datos para usar en el router
datos = Datos()


@router.get("/")
def read_root():
    return {"mensaje": "API de la biblioteca"}


@router.post(
    "/libros",
    response_model=Libro,
    status_code=201,
    description="Crear un nuevo libro",
    responses={
        **error_responses,
    },
)
def crear_libro(libro: LibroCreate) -> Libro:
    return datos.agregar_libro(libro)


@router.get(
    "/libros",
    response_model=LibrosPaginados,
    description="Obtener todos los libros",
    responses={
        422: error_responses[422],
    },
)
def obtener_libros(
    filtros: Annotated[LibroFiltros, Query()],
) -> LibrosPaginados:
    return datos.obtener_libros(filtros)


@router.get(
    "/libros/estadisticas",
    response_model=dict[str, int],
    description="Obtener las estadísticas de los libros",
)
def obtener_estadisticas_libros() -> dict[str, int]:
    return datos.estadisticas_libros()


@router.get(
    "/libros/{id}",
    response_model=Libro,
    description="Obtener un libro por su id",
    responses={
        404: error_responses[404],
        422: error_responses[422],
    },
)
def obtener_libro_por_id(id: int) -> Libro:
    return datos.obtener_libro_por_id(id)


@router.delete(
    "/libros/{id}",
    status_code=204,
    description="Eliminar un libro por su id",
    responses={
        404: error_responses[404],
        422: error_responses[422],
    },
)
def eliminar_libro(id: int) -> Response:
    return datos.eliminar_libro(id)


@router.patch(
    "/libros/{id}",
    response_model=Libro,
    description="Actualizar un libro por su id",
    responses={
        **error_responses,
    },
)
def actualizar_libro_parcial(id: int, libro: LibroParametros) -> Libro:
    return datos.actualizar_libro_parcial(id, libro)


@router.put(
    "/libros/{id}",
    response_model=Libro,
    description="Actualizar un libro por su id",
    responses={
        **error_responses,
    },
)
def actualizar_libro_total(id: int, libro: LibroCreate) -> Libro:
    return datos.actualizar_libro_total(id, libro)


@router.post(
    "/libros/{id}/prestar",
    response_model=Libro,
    description="Prestar un libro por su id",
    responses={
        404: error_responses[404],
        422: error_responses[422],
    },
)
def prestar_libro(id: int) -> Libro:
    return datos.prestar_libro(id)


@router.post(
    "/libros/{id}/devolver",
    response_model=Libro,
    description="Devolver un libro por su id",
    responses={
        404: error_responses[404],
        422: error_responses[422],
    },
)
def devolver_libro(id: int) -> Libro:
    return datos.devolver_libro(id)
