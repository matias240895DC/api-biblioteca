from pydantic import BaseModel

from datos.schemas.schemas import Libro


class Response(BaseModel):
    detail: str

    @staticmethod
    def post_response():
        return {
            "model": Libro,
            "status_code": 201,
            "description": "Libro creado correctamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "titulo": "el principito",
                        "autor": "antoine de saint-exupery",
                        "anio": 1943,
                        "disponible": True,
                    }
                }
            },
        }

    def error404(
        self, detail: str = "El libro no existe", description: str = "No encontrado"
    ):
        return {
            "model": Response,
            "description": description,
            "content": {
                "application/json": {
                    "example": {
                        "detail": detail,
                    }
                }
            },
        }

    def error409(
        self, detail: str = "El libro ya existe", description: str = "Conflicto"
    ):
        return {
            "model": Response,
            "description": description,
            "content": {
                "application/json": {
                    "example": {
                        "detail": detail,
                    }
                }
            },
        }

    def error422(self, description: str = "Datos inválidos según el esquema"):
        return {
            "model": Response,
            "description": description,
            "content": {
                "application/json": {
                    "examples": {
                        "titulo_faltante": {
                            "summary": "Falta el título",
                            "value": {"detail": ["El titulo es obligatorio"]},
                        },
                        "autor_faltante": {
                            "summary": "Falta el autor",
                            "value": {"detail": ["El autor es obligatorio"]},
                        },
                        "anio_fuera_de_rango": {
                            "summary": "Año menor a 1000 o mayor a 2100",
                            "value": {"detail": ["El año debe ser entre 1000 y 2100"]},
                        },
                        "anio_no_entero": {
                            "summary": 'Año que no es número (ej. "abc")',
                            "value": {"detail": ["El año debe ser un número entero"]},
                        },
                        "key_extra": {
                            "summary": "Campo que no existe en el schema",
                            "value": {"detail": ["Key inválida: 'autori'"]},
                        },
                    }
                }
            },
        }


class ResponseGet(Response):
    # Sobreescribe el 422 del padre: query params del GET /libros
    def error422(self, description: str = "Query params inválidos"):
        return {
            "model": Response,
            "description": description,
            "content": {
                "application/json": {
                    "examples": {
                        "desde_negativo": {
                            "summary": "Query key 'desde' menor que 0",
                            "value": {
                                "detail": [
                                    "La key 'desde' no puede ser negativa (ej. ?desde=-1)"
                                ]
                            },
                        },
                        "limite_invalido": {
                            "summary": "Query key 'limite' fuera de 1–100",
                            "value": {
                                "detail": [
                                    "La key 'limite' debe ser entre 1 y 100 (ej. ?limite=0)"
                                ]
                            },
                        },
                        "limite_no_entero": {
                            "summary": "Query key 'limite' no numérica",
                            "value": {
                                "detail": [
                                    "La key 'limite' debe ser un número entero (ej. ?limite=abc)"
                                ]
                            },
                        },
                        "titulo_tipo_invalido": {
                            "summary": "Query key 'titulo' con tipo inválido",
                            "value": {
                                "detail": [
                                    "La key 'titulo' debe ser una cadena de texto"
                                ]
                            },
                        },
                        "autor_tipo_invalido": {
                            "summary": "Query key 'autor' con tipo inválido",
                            "value": {
                                "detail": [
                                    "La key 'autor' debe ser una cadena de texto"
                                ]
                            },
                        },
                        "anio_no_entero": {
                            "summary": "Query key 'anio' (no 'año') no es número",
                            "value": {
                                "detail": [
                                    "La key 'anio' debe ser un número entero (ej. ?anio=abc). Usar 'anio', no 'año'"
                                ]
                            },
                        },
                        "disponible_invalido": {
                            "summary": "Query key 'disponible' no booleana",
                            "value": {
                                "detail": [
                                    "La key 'disponible' debe ser true o false (ej. ?disponible=talvez)"
                                ]
                            },
                        },
                        "key_extra": {
                            "summary": "Query key inexistente (ej. 'autori' o 'año')",
                            "value": {
                                "detail": [
                                    "Key inválida: 'año' (la correcta es 'anio')"
                                ]
                            },
                        },
                    }
                }
            },
        }


class ResponseGetById(Response):
    def error422(self, description: str = "Path param 'id' inválido"):
        return {
            "model": Response,
            "description": description,
            "content": {
                "application/json": {
                    "examples": {
                        "id_no_entero": {
                            "summary": "Path key 'id' no es número (ej. /libros/abc)",
                            "value": {
                                "detail": ["La key 'id' debe ser un número entero"]
                            },
                        },
                        "id_menor_igual_cero": {
                            "summary": "Path key 'id' <= 0 (ej. /libros/0)",
                            "value": {
                                "detail": ["La key 'id' no puede ser menor o igual a 0"]
                            },
                        },
                    }
                }
            },
        }
