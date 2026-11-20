from pydantic import BaseModel, ConfigDict, Field, field_validator


class LibroCreate(BaseModel):
    model_config = ConfigDict(validate_default=True)

    titulo: str | None = None
    autor: str | None = None
    anio: int | None = None
    disponible: bool | None = None

    @field_validator("titulo", mode="before")
    def validar_longitud_titulo(cls, v):

        if v is None:
            raise ValueError("El titulo es obligatorio")
        if not isinstance(v, str):
            raise ValueError("El titulo debe ser una cadena de texto")

        if v.strip() == "":
            raise ValueError("El titulo no puede estar vacío")

        if len(v) < 3 or len(v) > 100:
            raise ValueError("La longitud debe ser entre 3 y 100 caracteres")
        return v

    @field_validator("autor", mode="before")
    def validar_longitud_autor(cls, v):
        if v is None:
            raise ValueError("El autor es obligatorio")
        if not isinstance(v, str):

            raise ValueError("El autor debe ser una cadena de texto")
        if v.strip() == "":
            raise ValueError("El autor no puede estar vacío")

        if len(v) < 5 or len(v) > 100:
            raise ValueError("La longitud debe ser entre 5 y 100 caracteres")
        return v

    @field_validator("anio", mode="before")
    def validar_anio(cls, v):

        if v is None:
            raise ValueError("El año es obligatorio")

        if isinstance(v, str) and v.strip().isdigit():
            v = int(v)
        if not isinstance(v, int):
            raise ValueError("El año debe ser un número entero")

        if v < 1000 or v > 2100:
            raise ValueError("El año debe ser entre 1000 y 2100")
        return v

    @field_validator("disponible", mode="before")
    def validar_disponible(cls, v):
        if v is None:
            return None  # no se valida si el disponible es None
        if not isinstance(v, bool):
            raise ValueError("El disponible debe ser un booleano")

        if isinstance(v, str):
            valor = v.strip().lower()
            if valor in ("true", "1"):
                return True
            if valor in ("false", "0"):
                return False
            raise ValueError("El disponible debe ser True o False")
        return v


class Libro(LibroCreate):
    id: int
    disponible: bool = Field(default=True)


class LibrosPaginados(BaseModel):
    data: list[Libro]  # los libros de esta página
    limite: int  # cantidad de libros por página
    desde: int  # página actual
    total: int  # total de libros en la biblioteca


class LibroParametros(BaseModel):
    model_config = ConfigDict(validate_default=True)

    titulo: str | None = None
    autor: str | None = None
    anio: int | None = None
    disponible: bool | None = None


class LibroFiltros(LibroParametros):

    desde: int = 0
    limite: int = 100

    @field_validator("desde", mode="before")
    def validar_desde(cls, v):
        if v is None or v == "":
            return 0
        v = int(v)  # primero convertir
        if v < 0:
            raise ValueError("El desde no puede ser negativo")
        return v

    @field_validator("limite", mode="before")
    def validar_limite(cls, v):
        if v is None or v == "":
            return 100
        v = int(v)
        if v < 1 or v > 100:
            raise ValueError("El limite debe ser entre 1 y 100")
        return v
