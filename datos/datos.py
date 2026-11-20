import json
from pathlib import Path

from fastapi import HTTPException, Response

from datos.schemas.schemas import (
    Libro,
    LibroCreate,
    LibroFiltros,
    LibroParametros,
    LibrosPaginados,
)


class Datos:
    def __init__(self):
        self.libros = []
        self.id_siguiente = 0

        carpeta = (
            Path(__file__).resolve().parent
        )  # carpeta donde está este archivo (datos.py) → .../api-biblioteca/datos
        carpeta.mkdir(parents=True, exist_ok=True)  # 1) asegura que exista la carpeta
        self.archivo_libros = (
            carpeta / "libros.json"
        )  # 2) archivo donde se guardan los libros
        self.cargar_libros()

    def obtener_libros(
        self,
        filtros: LibroFiltros,
    ) -> LibrosPaginados:
        filtrados = [
            libro
            for libro in self.libros
            if (
                filtros.titulo is None
                or (
                    libro.titulo is not None
                    and libro.titulo.lower() == filtros.titulo.lower()
                )
            )
            and (
                filtros.autor is None
                or (
                    libro.autor is not None
                    and libro.autor.lower() == filtros.autor.lower()
                )
            )
            and (filtros.anio is None or libro.anio == filtros.anio)
            and (filtros.disponible is None or libro.disponible == filtros.disponible)
        ]
        total = len(filtrados)  # total de libros filtrados
        data = filtrados[filtros.desde : filtros.desde + filtros.limite]
        return LibrosPaginados(
            data=data, limite=filtros.limite, desde=filtros.desde, total=total
        )

    def obtener_libro_por_id(self, id: int) -> Libro:
        if id < 1:
            raise HTTPException(
                status_code=422, detail="El id ingresado no puede ser menor o igual a 0"
            )
        for libro in self.libros:
            if libro.id == id:
                return libro
        raise HTTPException(
            status_code=404,
            detail="El id ingresado es inexistente, no se encontró el libro",
        )

    def buscar_libro_por_titulo(self, titulo: str, id: int) -> bool:
        return any(
            (item.titulo is not None and item.titulo.lower() == titulo.lower())
            and item.id != id
            for item in self.libros
        )

    def buscar_libro_por_autor_y_titulo(self, autor: str, titulo: str) -> bool:
        return any(
            (item.autor is not None and item.autor.lower() == autor.lower())
            and (item.titulo is not None and item.titulo.lower() == titulo.lower())
            for item in self.libros
        )

    def validar_autor_y_titulo_unico(self, autor: str, titulo: str, id: int) -> bool:
        return any(
            (item.autor is not None and item.autor.lower() == autor.lower())
            and (item.titulo is not None and item.titulo.lower() == titulo.lower())
            and item.id != id
            for item in self.libros
        )

    def agregar_libro(self, libro: LibroCreate) -> Libro:
        if (
            libro.autor
            and libro.titulo
            and self.buscar_libro_por_autor_y_titulo(libro.autor, libro.titulo)
        ):
            raise HTTPException(
                status_code=409, detail="El autor y el nombre del libro ya existe"
            )
        self.id_siguiente = self.id_siguiente + 1
        nuevo_libro = Libro(
            id=self.id_siguiente,
            titulo=libro.titulo.lower() if libro.titulo else None,
            autor=libro.autor.lower() if libro.autor else None,
            anio=libro.anio,
            disponible=True,
        )
        # Obtener el id del libro más grande o 0 si no hay libros y sumarle 1
        self.libros.append(nuevo_libro)
        self.guardar()
        return nuevo_libro

    def eliminar_libro(self, id):
        libro = self.obtener_libro_por_id(id)
        self.libros.remove(libro)
        self.guardar()
        return Response(status_code=204)

    def actualizar_libro_parcial(self, id: int, libro: LibroParametros) -> Libro:
        libro_existente = self.obtener_libro_por_id(id)
        datos = libro.model_dump(exclude_unset=True)
        for campo, valor in datos.items():
            setattr(libro_existente, campo, valor)
        self.guardar()
        return libro_existente

    def actualizar_libro_total(self, id: int, libro: LibroCreate) -> Libro:
        libro_existente = self.obtener_libro_por_id(id)
        if (
            libro.autor
            and libro.titulo
            and self.validar_autor_y_titulo_unico(libro.autor, libro.titulo, id)
        ):
            raise HTTPException(
                status_code=409, detail="El autor y el nombre del libro ya existe"
            )
        datos = libro.model_dump()
        if datos.get("disponible") is None:
            datos["disponible"] = libro_existente.disponible

        for campo, valor in datos.items():
            setattr(libro_existente, campo, valor)
        self.guardar()
        return libro_existente

    def prestar_libro(self, id: int) -> Libro:
        libro = self.obtener_libro_por_id(id)
        if libro.disponible:
            libro.disponible = False
            self.guardar()
            return libro
        else:
            raise HTTPException(
                status_code=409,
                detail=f"El libro con el titulo: {libro.titulo} no está disponible",
            )

    def devolver_libro(self, id: int) -> Libro:
        libro = self.obtener_libro_por_id(id)
        if not libro.disponible:
            libro.disponible = True
            self.guardar()
            return libro
        else:
            raise HTTPException(
                status_code=409,
                detail=f"El libro con el titulo: {libro.titulo} ya está disponible ",
            )

    def estadisticas_libros(self) -> dict[str, int]:
        return {
            "total_libros": len(self.libros),
            "total_libros_disponibles": len(
                [libro for libro in self.libros if libro.disponible]
            ),
            "total_libros_prestados": len(
                [libro for libro in self.libros if not libro.disponible]
            ),
        }

    def guardar(self):
        lista = [libro.model_dump() for libro in self.libros]
        self.archivo_libros.write_text(
            json.dumps(lista, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def cargar_libros(self):
        self.libros = []
        self.id_siguiente = 0

        if not self.archivo_libros.exists():
            return

        try:
            data = json.loads(self.archivo_libros.read_text(encoding="utf-8") or "[]")
            if not isinstance(data, list):
                return
            self.libros = [Libro.model_validate(item) for item in data]
            if self.libros:
                self.id_siguiente = max(libro.id for libro in self.libros)
        except (json.JSONDecodeError, OSError, ValueError):
            self.libros = []
            self.id_siguiente = 0
