from pydantic import BaseModel


class ErrorDetail(BaseModel):
    detail: str


def error404():

    return {
        "model": ErrorDetail,
        "description": "El libro no existe",
        "content": {
            "application/json": {
                "example": {
                    "detail": "El libro no existe",
                }
            }
        },
    }


def error409():
    return {
        "model": ErrorDetail,
        "description": "El libro ya existe",
        "content": {
            "application/json": {
                "example": {
                    "detail": "El libro ya existe",
                }
            }
        },
    }


def error422():
    return {
        "model": ErrorDetail,
        "description": "Error de validación (campos obligatorios, id inválido, etc.)",
        "content": {
            "application/json": {
                "examples": {
                    "campo_obligatorio": {
                        "summary": "Falta un campo obligatorio",
                        "value": {"detail": ["El título es obligatorio"]},
                    },
                    "id_invalido": {
                        "summary": "Id menor o igual a 0",
                        "value": {
                            "detail": "El id ingresado no puede ser menor o igual a 0"
                        },
                    },
                }
            }
        },
    }


error_responses = {
    404: error404(),
    409: error409(),
    422: error422(),
}
