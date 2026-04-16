from flask import Blueprint, jsonify, request
import mysql.connector
from mysql.connector import errorcode
from backend.db import db
from backend.routes.utils import (
    BAD_REQUEST_CODE,
    CONFLICT_CODE,
    NO_CONTENT_CODE,
    NOT_FOUND_CODE,
    OK_CODE,
    crear_error,
)
from backend.routes.validadores import (
    validar_equipo,
    validar_fase,
    validar_fecha,
    validar_id,
    validar_limit,
    validar_offset,
    validar_partido,
)

partidos_blueprint = Blueprint("partidos", __name__)


@partidos_blueprint.route("/partidos", methods=["GET"])
def obtener_partido():
    equipo = validar_equipo(request.args.get("equipo"))
    fecha = validar_fecha(request.args.get("fecha"))
    fase = validar_fase(request.args.get("fase"))
    limit = validar_limit(request.args.get("_limit"))
    offset = validar_offset(request.args.get("_offset"))
    valores = {
        "equipo": equipo,
        "fecha": fecha,
        "fase": fase,
        "limit": limit,
        "offset": offset,
    }

    query = "SELECT equipo_local, equipo_visitante, fase, DATE_FORMAT(fecha, '%Y-%m-%d') as fecha, id FROM partidos"
    wheres = ""

    if equipo:
        query_equipo = "equipo_local=%(equipo)s OR equipo_visitante=%(equipo)s"
        wheres += query_equipo if wheres == "" else f" AND {query_equipo}"
    if fecha:
        query_fecha = "fecha=%(fecha)s"
        wheres += query_fecha if wheres == "" else f" AND {query_fecha}"
    if fase:
        query_fase = "fase=%(fase)s"
        wheres += query_fase if wheres == "" else f" AND {query_fase}"

    query += f" WHERE {wheres}" if wheres != "" else ""

    query += f" LIMIT %(limit)s OFFSET %(offset)s"

    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(query, valores)
        partidos = cursor.fetchall()
        db.commit()
    finally:
        cursor.close()

    if len(partidos) == 0:
        if wheres != "":
            raise RuntimeError(
                [
                    crear_error(
                        NOT_FOUND_CODE,
                        "NOT FOUND",
                        f"la busqueda con {valores} no retornó resultados",
                    )
                ]
            )
        else:
            return "", NO_CONTENT_CODE
    else:
        return jsonify(partidos=partidos), 200


@partidos_blueprint.route("/partidos", methods=["POST"])
def crear_partidos():
    nuevo_partido = validar_partido(request.get_json())

    query = "INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase) VALUES (%(equipo_local)s, %(equipo_visitante)s, %(fecha)s, %(fase)s) "
    cursor = db.cursor()
    try:
        cursor.execute(query, nuevo_partido)
        db.commit()
        return "", 204
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_DUP_ENTRY:
            raise RuntimeError(
                [
                    crear_error(
                        CONFLICT_CODE,
                        "CONFLICT",
                        f"el partido con valores {nuevo_partido} ya existe",
                    )
                ]
            )
        else:
            raise error
    finally:
        cursor.close()


@partidos_blueprint.route("/partidos/<int:id_crudo>", methods=["GET"])
def obtener_partidos_id(id_crudo):
    id = validar_id(id_crudo)

    query = "SELECT equipo_local, equipo_visitante, fase, DATE_FORMAT(fecha, '%Y-%m-%d') as fecha, id, goles_equipo_local, goles_equipo_visitante FROM partidos WHERE id=%(id)s"
    values = {"id": id}

    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(query, values)
        partido = dict(cursor.fetchone())
        db.commit()
    finally:
        cursor.close()

    if partido == None:
        raise RuntimeError(
            [
                crear_error(
                    NOT_FOUND_CODE, "NOT FOUND", f"No existe partido con id: {id}"
                )
            ]
        )

    goles_equipo_local = partido.get("goles_equipo_local")
    goles_equipo_visitante = partido.get("goles_equipo_visitante")
    if goles_equipo_local != -1 and goles_equipo_visitante != -1:
        partido.update(
            {
                "resultado": {
                    "local": goles_equipo_local,
                    "visitante": goles_equipo_visitante,
                },
            }
        )
    else:
        partido.update({"resultado": None})

    print(partido)
    partido.pop("goles_equipo_local", None)
    partido.pop("goles_equipo_visitante", None)

    return jsonify(partido), OK_CODE


@partidos_blueprint.route("/partidos/<int:id_crudo>", methods=["DELETE"])
def borrar_partido_id(id_crudo):
    id = validar_id(id_crudo)

    query = "DELETE FROM partidos WHERE id=%(id)s"
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
                        NOT_FOUND_CODE, "NOT FOUND", f"no existe partidos con id: {id}"
                    )
                ]
            )

        db.commit()
        return "", NO_CONTENT_CODE
    finally:
        cursor.close()


@partidos_blueprint.route("/partidos/<int:id_crudo>", methods=["PATCH"])
def reparar_partidos_id(id_crudo):
    id = validar_id(id_crudo)
    body = request.get_json()
    equipo_local = validar_equipo(body.get("equipo_local", ""))
    equipo_visitante = validar_equipo(body.get("equipo_visitante", ""))
    fase = validar_fase(body.get("fase", ""))
    fecha = validar_fecha(body.get("fecha", ""))

    query = "UPDATE partidos SET"
    sets = ""
    sets += " equipo_local = %(equipo_local)s," if equipo_local else ""
    sets += " equipo_visitante = %(equipo_visitante)s," if equipo_visitante else ""
    sets += " fase = %(fase)s," if fase else ""
    sets += " fecha = %(fecha)s," if fecha else ""

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

    print(query)

    values = {
        "id": id,
        "equipo_local": equipo_local,
        "equipo_visitante": equipo_visitante,
        "fase": fase,
        "fecha": fecha,
    }

    cursor = db.cursor()
    try:
        cursor.execute(query, values)
        if cursor.rowcount == 0:
            raise RuntimeError(
                [
                    crear_error(
                        NOT_FOUND_CODE, "NOT FOUND", f"no existe partidos con id: {id}"
                    )
                ]
            )

        db.commit()
        return "", 204
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_DUP_ENTRY:
            raise RuntimeError(
                [
                    crear_error(
                        CONFLICT_CODE,
                        "CONFLICT",
                        f"el partido con valores {values} ya existe",
                    )
                ]
            )
        else:
            raise error
    finally:
        cursor.close()


@partidos_blueprint.route("/partidos/<int:id_crudo>", methods=["PUT"])
def remplazar_partidos_id(id_crudo):
    id = validar_id(id_crudo)
    nuevo_partido = validar_partido(request.get_json())
    nuevo_partido.update({"id": id})

    query = "UPDATE partidos SET equipo_local = %(equipo_local)s, equipo_visitante = %(equipo_visitante)s, fase = %(fase)s, fecha = %(fecha)s WHERE id=%(id)s"

    cursor = db.cursor()
    try:
        cursor.execute(query, nuevo_partido)
        if cursor.rowcount == 0:
            raise RuntimeError(
                [
                    crear_error(
                        NOT_FOUND_CODE, "NOT FOUND", f"no existe partidos con id: {id}"
                    )
                ]
            )

        db.commit()
        return "", 204
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_DUP_ENTRY:
            raise RuntimeError(
                [
                    crear_error(
                        CONFLICT_CODE,
                        "CONFLICT",
                        f"el partido con valores {nuevo_partido} ya existe",
                    )
                ]
            )
        else:
            raise error
    finally:
        cursor.close()
