from flask import Blueprint, jsonify, request
from backend.db import db

partidos_blueprint = Blueprint("partidos", __name__)

@partidos_blueprint.route("/partidos", methods=["GET"])
def obtener_partido():
    equipo = request.args.get("equipo")
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM partidos WHERE equipo_local=%s OR equipo_visitante=%s",
        (equipo, equipo)
    )
    resultados = cursor.fetchall()
    cursor.close()
    return jsonify(partidos=resultados), 200

@partidos_blueprint.route("/partidos", methods=["POST"])
def crear_partidos():
    datos = request.get_json() 
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO partidos (equipo_local, equipo_visitante, ciudad, fecha, estadio, fase) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (
            datos["equipo_local"],
            datos["equipo_visitante"],
            datos.get("ciudad"),
            datos.get("fecha"),
            datos.get("estadio"),
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
        "SELECT * FROM partidos WHERE id_eq1=%s OR id_eq2=%s",
        (id, id)
    )
    partido = cursor.fetchall()
    cursor.close()
    return jsonify(partido), 200

@partidos_blueprint.route("/partidos", methods=["DELETE"])     
def borrar_partido_id(id_partido):
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM partidos WHERE id_partido=%s"
        )
    db.commit()
    cursor.close()
    return jsonify(id_partido), 204

