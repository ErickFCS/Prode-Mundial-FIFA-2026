OK_CODE = 200
CREATED_CODE = 201
NO_CONTENT_CODE = 204
BAD_REQUEST_CODE = 400
NOT_FOUND_CODE = 404
CONFLICT_CODE = 409
INTERNAL_ERROR_CODE = 500

FASES_VALIDAS = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]


def crear_error(code, description, message, level="error"):
    return {
        "code": code,
        "description": description,
        "level": level,
        "message": message,
    }
