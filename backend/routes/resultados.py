from flask import Blueprint, request
from backend.db import db
from backend.utils import (
    NO_CONTENT_CODE,
    NOT_FOUND_CODE,
    NOT_FOUND_CODE_MESSAGE,
    crear_error,
)
from backend.validadores import (
    validar_id,
    validar_resultado,
)

resultados_blueprint = Blueprint("resultados", __name__)


@resultados_blueprint.route("/partidos/<int:id_crudo>/resultado", methods=["PUT"])
def partidos_id_resultado_put(id_crudo):
    id = validar_id(id_crudo)
    nuevo_resultado = validar_resultado(request.get_json())
    nuevo_resultado.update({"id": id})

    query = "UPDATE partidos SET goles_equipo_local = %(local)s, goles_equipo_visitante = %(visitante)s WHERE id=%(id)s"

    cursor = db.cursor()
    try:
        cursor.execute(query, nuevo_resultado)
        if cursor.rowcount == 0:
            raise RuntimeError(
                [
                    crear_error(
                        NOT_FOUND_CODE, NOT_FOUND_CODE_MESSAGE, f"no existe partido con id: {id}"
                    )
                ]
            )

        db.commit()
        return "", NO_CONTENT_CODE
    except Exception as error:
        db.rollback()
        raise error
    finally:
        cursor.close()
