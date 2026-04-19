from datetime import datetime
from flask import Blueprint, request
import mysql.connector
from mysql.connector import errorcode
from backend.db import db

from backend.utils import (
    CONFLICT_CODE,
    CONFLICT_CODE_MESSAGE,
    CREATED_CODE,
    NOT_FOUND_CODE,
    NOT_FOUND_CODE_MESSAGE,
    crear_error,
)
from backend.validadores import validar_id, validar_prediccion

predicciones_blueprint = Blueprint("predicciones", __name__)


@predicciones_blueprint.route("/partidos/<int:id_crudo>/prediccion", methods=["POST"])
def crear_prediccion(id_crudo):
    id = validar_id(id_crudo)
    prediccion = validar_prediccion(request.get_json())
    prediccion.update({"id_partido": id})

    cursor = db.cursor(dictionary=True)
    try:
        query_buscar_partido = "SELECT id FROM partidos WHERE id = %(id_partido)s"

        cursor.execute(query_buscar_partido, prediccion)
        partido = cursor.fetchone()

        if not partido:
            raise RuntimeError(
                [
                    crear_error(
                        NOT_FOUND_CODE,
                        NOT_FOUND_CODE_MESSAGE,
                        f"no existe partido con id: {id}",
                    )
                ]
            )

        if partido.get("fecha") < datetime.now():
            raise RuntimeError(
                [
                    crear_error(
                        CONFLICT_CODE,
                        CONFLICT_CODE_MESSAGE,
                        "No se puede predecir en un partido ya jugado",
                    )
                ]
            )

        query_principal = "INSERT INTO predicciones (id_usuario, id_partido, goles_local, goles_visitante) VALUES (%(id_usuario)s, %(id_partido)s, %(goles_local)s, %(goles_visitante)s)"

        cursor.execute(query_principal, prediccion)

        db.commit()

        return "", CREATED_CODE

    except mysql.connector.Error as error:
        db.rollback()
        if error.errno == errorcode.ER_DUP_ENTRY:
            raise RuntimeError(
                [
                    crear_error(
                        CONFLICT_CODE,
                        CONFLICT_CODE_MESSAGE,
                        f"El usuario con id: {prediccion.get("id_usuario")} ya tiene una prediccion hecha",
                    )
                ]
            )
        elif error.errno == errorcode.ER_NO_REFERENCED_ROW_2:
            raise RuntimeError(
                [
                    crear_error(
                        CONFLICT_CODE,
                        CONFLICT_CODE_MESSAGE,
                        f"No existe usuario con id: {prediccion.get("id_usuario")}",
                    )
                ]
            )
        else:
            raise error
    except Exception as error:
        db.rollback()
        raise error
    finally:
        cursor.close()
