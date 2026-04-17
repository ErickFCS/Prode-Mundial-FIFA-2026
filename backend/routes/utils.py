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

def construir_links(base_url, limit, offset, db_count):
    first_offset = 0
    prev_offset = max(offset - limit, 0)
    next_offset = offset + limit
    last_offset = db_count - limit

    return {
        "_first": {"href": f"{base_url}?_limit={limit}&_offset={first_offset}"},
        "_prev": {"href": f"{base_url}?_limit={limit}&_offset={prev_offset}"},
        "_next": {"href": f"{base_url}?_limit={limit}&_offset={next_offset}"},
        "_last": {"href": f"{base_url}?_limit={limit}&_offset={last_offset}"}
    }

