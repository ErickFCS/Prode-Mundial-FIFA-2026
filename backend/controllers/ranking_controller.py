from flask import Blueprint, jsonify, request

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

    predicciones = [
        {"id_usuario": 1, "id_partido": 1, "local": 2, "visitante": 1},
        {"id_usuario": 2, "id_partido": 1, "local": 1, "visitante": 0},
        {"id_usuario": 1, "id_partido": 2, "local": 0, "visitante": 0},
    ]

    resultados = {
        1: {"local": 2, "visitante": 1},
        2: {"local": 1, "visitante": 1}
    }

    ranking_lista = calcular_ranking(predicciones, resultados)
   
    ranking_lista = ranking_lista[offset: offset + limit]

    links = construir_links(limit, offset)

    response = {
        "ranking": ranking_lista,
        "_links": _links
    }

    return jsonify(response), 200
