from flask import Blueprint, jsonify, request
from backend.db import db

ranking_blueprint = Blueprint("ranking", __name__)


def resultado(local, visitante):
    if local > visitante:
        return 1
    elif local < visitante:
        return -1
    else:
        return 0

def calcular_puntos(pred, real):
    pred_res = resultado(pred["local"], pred["visitante"])
    real_res = resultado(real["local"], real["visitante"])

    if pred["local"] == real["local"] and pred["visitante"] == real["visitante"]:
        return 3
    elif pred_res == real_res:
        return 1
    return 0

def calcular_ranking(predicciones, resultados):
    ranking = {}

    for pred in predicciones:
        usuario = pred["id_usuario"]
        partido_id = pred["id_partido"]

        real = resultados.get(partido_id)
        if not real:
            continue

        puntos = calcular_puntos(pred, real)

        ranking[usuario] = ranking.get(usuario, 0) + puntos

    ranking_lista = [
        {"id_usuario": user, "puntos": pts}
        for user, pts in ranking.items()
    ]

    ranking_lista.sort(key=lambda x: x["puntos"], reverse=True)

    return ranking_lista

def construir_links(limit, offset):
    base_url = "/ranking"

    first_offset = 0
    prev_offset = max(offset - limit, 0)
    next_offset = offset + limit

    return {
        "_first": {"href": f"{base_url}?_limit={limit}&_offset={first_offset}"},
        "_prev": {"href": f"{base_url}?_limit={limit}&_offset={prev_offset}"},
        "_next": {"href": f"{base_url}?_limit={limit}&_offset={next_offset}"},
        # calcular last_offset correctamente cuando tenga total desde db
        "_last": {"href": f"{base_url}?_limit={limit}&_offset={offset}"}
    }


@ranking_blueprint.route("/ranking", methods=["GET"])
def ranking_get():

    limit = request.args.get("_limit", default=10, type=int)
    offset = request.args.get("_offset", default=0, type=int)

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.id_usuario,
            p.id_partido,
            p.goles_equipo_local AS pred_local,
            p.goles_equipo_visitante AS pred_visitante,
            pa.goles_equipo_local AS real_local,
            pa.goles_equipo_visitante AS real_visitante
        FROM predicciones p
        JOIN partidos pa ON p.id_partido = pa.id
    """)

    filas = cursor.fetchall()
    cursor.close()

    predicciones = []
    resultados = {}

    for fila in filas:
    
        if fila["real_local"] == -1 or fila["real_visitante"] == -1:
            continue

        predicciones.append({
            "id_usuario": fila["id_usuario"],
            "id_partido": fila["id_partido"],
            "local": fila["pred_local"],
            "visitante": fila["pred_visitante"]
        })

        if fila["id_partido"] not in resultados:
            resultados[fila["id_partido"]] = {
                "local": fila["real_local"],
                "visitante": fila["real_visitante"]
            }

    ranking_lista = calcular_ranking(predicciones, resultados)
   
    ranking_lista = ranking_lista[offset: offset + limit]

    links = construir_links(limit, offset)

    response = {
        "ranking": ranking_lista,
        "_links": links
    }

    return jsonify(response), 200
