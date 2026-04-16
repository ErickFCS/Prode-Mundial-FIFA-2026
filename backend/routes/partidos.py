import re
from flask import Blueprint, jsonify, request
from backend.db import db
from backend.routes.utils import (
    BAD_REQUEST_CODE,
    FASES_VALIDAS,
    NO_CONTENT_CODE,
    NOT_FOUND_CODE,
    crear_error,
)

partidos_blueprint = Blueprint("partidos", __name__)


def validar_equipo(equipo):
    if not equipo:
        return ""

    return equipo


def validar_fecha(fecha):
    if not fecha:
        return ""

    errores = []
    formato_acceptado = re.compile(r"\d\d\d\d-\d\d-\d\d")
    if not formato_acceptado.fullmatch(fecha):
        errores.append(
            crear_error(
                BAD_REQUEST_CODE,
                "BAD REQUEST",
                f"{fecha} no respeta el formato YYYY-MM-DD",
            )
        )
    anio, mes, dia = list(map(int, fecha.split("-")))
    if dia <= 0 or dia > 31:
        errores.append(
            crear_error(BAD_REQUEST_CODE, "BAD REQUEST", f"{dia} no esta entre 1 y 31")
        )
    if mes > 12 or mes < 1:
        errores.append(
            crear_error(BAD_REQUEST_CODE, "BAD REQUEST", f"{mes} no esta entre 1 y 12")
        )
    if anio > 9999 or anio < 1000:
        errores.append(
            crear_error(
                BAD_REQUEST_CODE, "BAD REQUEST", f"{anio} no esta entre 1000 y 9999"
            )
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return fecha


def validar_fase(fase):
    if not fase:
        return ""

    errores = []
    if fase not in FASES_VALIDAS:
        errores.append(
            crear_error(
                BAD_REQUEST_CODE, "BAD REQUEST", f"{fase} no esta entre {FASES_VALIDAS}"
            )
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return fase


def validar_limit(limit_crudo):
    if not limit_crudo:
        return 10

    limit = int(limit_crudo)

    errores = []
    if limit <= 0:
        errores.append(
            crear_error(BAD_REQUEST_CODE, "BAD REQUEST", f"{limit} no es mayor a 0")
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return limit


def validar_offset(offset_crudo):
    if not offset_crudo:
        return 0

    offset = int(offset_crudo)

    errores = []
    if offset < 0:
        errores.append(
            crear_error(BAD_REQUEST_CODE, "BAD REQUEST", f"{offset} es menor a 0")
        )

    if len(errores) > 0:
        raise RuntimeError(errores)

    return offset


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

    query = "SELECT equipo_local, equipo_visitante, fase, fecha, id FROM partidos"
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
    cursor.execute(
        "SELECT * FROM partidos WHERE equipo_local=%s OR equipo_visitante=%s",
        (equipo, equipo)
    )
    resultados = cursor.fetchall()
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
    datos = request.get_json() 
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase) "
        "VALUES (%s, %s, %s, %s)",
        (
            datos["equipo_local"],
            datos["equipo_visitante"],
            datos.get("fecha"),
            datos.get("fase")
        )
    )
    db.commit()
    cursor.close()
    return jsonify(mensaje="Partido agregado correctamente"), 204

@partidos_blueprint.route("/partidos", methods=["GET"])
def obtener_partidos_id():
    id = request.args.get("id")
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM partidos WHERE id=%s",
        (id,)
    )
    partido = cursor.fetchall()
    cursor.close()
    return jsonify(partido), 200

@partidos_blueprint.route("/partidos", methods=["DELETE"])     
def borrar_partido_id(id_partido):
    id = request.args.get("id")
    cursor = db.cursor()
    cursor.execute("DELETE FROM partidos WHERE id=%s",(id,))
    db.commit()
    cursor.close()
    return jsonify(id_partido), 204

