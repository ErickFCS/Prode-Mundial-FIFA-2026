from flask import Blueprint, jsonify, request
import mysql.connector
from mysql.connector import errorcode
from backend.db import db
from backend.utils import (
    BAD_REQUEST_CODE,
    CONFLICT_CODE,
    CREATED_CODE,
    NO_CONTENT_CODE,
    NOT_FOUND_CODE,
    OK_CODE,
    construir_links,
    crear_error,
)
from backend.validadores import (
    validar_equipo,
    validar_id,
    validar_limit,
    validar_offset,
    validar_usuario,
)

usuarios_blueprint = Blueprint("usuarios", __name__)


@usuarios_blueprint.route("/usuarios", methods=["GET"])
def obtener_usuario():
    limit = validar_limit(request.args.get("_limit"))
    offset = validar_offset(request.args.get("_offset"))
    valores = {
        "limit": limit,
        "offset": offset,
    }

    query = "SELECT id, nombre FROM usuarios LIMIT %(limit)s OFFSET %(offset)s"
    query_para_count = "SELECT count(*) as len FROM usuarios"

    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(query, valores)
        usuarios = cursor.fetchall()
        cursor.execute(query_para_count, valores)
        db_select = cursor.fetchone()
        db_count = 0 if db_select is None else db_select.get("len")
        db.commit()
    except Exception as error:
        db.rollback()
        raise error
    finally:
        cursor.close()

    if len(usuarios) == 0:
        return "", NO_CONTENT_CODE
    else:
        return (
            jsonify(
                _links=construir_links(request.base_url, limit, offset, db_count),
                usuarios=usuarios,
            ),
            200,
        )


@usuarios_blueprint.route("/usuarios", methods=["POST"])
def crear_usuarios():
    nuevo_usuario = validar_usuario(request.get_json())

    query = "INSERT INTO usuarios (nombre, email) VALUES (%(nombre)s, %(email)s)"
    cursor = db.cursor()
    try:
        cursor.execute(query, nuevo_usuario)
        db.commit()
        return "", CREATED_CODE
    except mysql.connector.Error as error:
        db.rollback()
        if error.errno == errorcode.ER_DUP_ENTRY:
            raise RuntimeError(
                [
                    crear_error(
                        CONFLICT_CODE,
                        "CONFLICT",
                        f"el usuario con valores {nuevo_usuario} ya existe",
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


@usuarios_blueprint.route("/usuarios/<int:id_crudo>", methods=["GET"])
def obtener_usuarios_id(id_crudo):
    id = validar_id(id_crudo)

    query = "SELECT email, id, nombre FROM usuarios WHERE id=%(id)s"
    values = {"id": id}

    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(query, values)
        usuario = cursor.fetchone()
        db.commit()
    except Exception as error:
        db.rollback()
        raise error
    finally:
        cursor.close()

    if usuario is None:
        raise RuntimeError(
            [
                crear_error(
                    NOT_FOUND_CODE, "NOT FOUND", f"No existe usuario con id: {id}"
                )
            ]
        )

    return jsonify(usuario), OK_CODE


@usuarios_blueprint.route("/usuarios/<int:id_crudo>", methods=["DELETE"])
def borrar_usuario_id(id_crudo):
    id = validar_id(id_crudo)

    query = "DELETE FROM usuarios WHERE id=%(id)s"
    values = {
        "id": id,
    }

    cursor = db.cursor()
    try:
        cursor.execute(query, values)
        if cursor.rowcount == 0:
            raise RuntimeError(
                [
                    crear_error(
                        NOT_FOUND_CODE, "NOT FOUND", f"no existe usuarios con id: {id}"
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


@usuarios_blueprint.route("/usuarios/<int:id_crudo>", methods=["PATCH"])
def reparar_usuarios_id(id_crudo):
    id = validar_id(id_crudo)
    body = request.get_json()
    email = validar_equipo(body.get("email", ""))
    nombre = validar_equipo(body.get("nombre", ""))

    query = "UPDATE usuarios SET"
    sets = ""
    sets += " email = %(email)s," if email else ""
    sets += " nombre = %(nombre)s," if nombre else ""

    if not sets:
        raise RuntimeError(
            [
                crear_error(
                    BAD_REQUEST_CODE, "BAD REQUEST", "no enviaste nada para reparar"
                )
            ]
        )

    sets = sets.rstrip(",")  # Remueve la ultima coma
    query += sets
    query += " WHERE id=%(id)s"

    values = {
        "id": id,
        "email": nombre,
        "nombre": nombre,
    }

    cursor = db.cursor()
    try:
        cursor.execute(query, values)
        if cursor.rowcount == 0:
            raise RuntimeError(
                [
                    crear_error(
                        NOT_FOUND_CODE, "NOT FOUND", f"no existe usuarios con id: {id}"
                    )
                ]
            )

        db.commit()
        return "", NO_CONTENT_CODE
    except mysql.connector.Error as error:
        db.rollback()
        if error.errno == errorcode.ER_DUP_ENTRY:
            raise RuntimeError(
                [
                    crear_error(
                        CONFLICT_CODE,
                        "CONFLICT",
                        f"el usuario con valores {values} ya existe",
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


@usuarios_blueprint.route("/usuarios/<int:id_crudo>", methods=["PUT"])
def remplazar_usuarios_id(id_crudo):
    id = validar_id(id_crudo)
    nuevo_usuario = validar_usuario(request.get_json())
    nuevo_usuario.update({"id": id})

    query = "UPDATE usuarios SET email = %(email)s, nombre = %(nombre)s WHERE id=%(id)s"

    cursor = db.cursor()
    try:
        cursor.execute(query, nuevo_usuario)
        if cursor.rowcount == 0:
            raise RuntimeError(
                [
                    crear_error(
                        NOT_FOUND_CODE, "NOT FOUND", f"no existe usuarios con id: {id}"
                    )
                ]
            )

        db.commit()
        return "", NO_CONTENT_CODE
    except mysql.connector.Error as error:
        db.rollback()
        if error.errno == errorcode.ER_DUP_ENTRY:
            raise RuntimeError(
                [
                    crear_error(
                        CONFLICT_CODE,
                        "CONFLICT",
                        f"el usuario con valores {nuevo_usuario} ya existe",
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
