from flask import Blueprint, jsonify, request

ranking_blueprint = Blueprint("ranking", __name__)


def resultado(local, visitante):
    if local > visitante:
        return 1
    elif local < visitante:
        return -1
    else:
        return 0


@ranking_blueprint.route("/ranking", methods=["GET"])
def ranking_get():

    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)

    predicciones = [
        {"id_usuario": 1, "id_partido": 1, "local": 2, "visitante": 1},
        {"id_usuario": 2, "id_partido": 1, "local": 1, "visitante": 0},
        {"id_usuario": 1, "id_partido": 2, "local": 0, "visitante": 0},
    ]

    resultados = {
        1: {"local": 2, "visitante": 1},
        2: {"local": 1, "visitante": 1}
    }

    ranking = {}

    for pred in predicciones:
        usuario = pred["id_usuario"]
        partido_id = pred["id_partido"]

        real = resultados.get(partido_id)

        if not real:
            continue

        puntos = 0

        pred_res = resultado(pred["local"], pred["visitante"])
        real_res = resultado(real["local"], real["visitante"])

        if pred["local"] == real["local"] and pred["visitante"] == real["visitante"]:
            puntos = 3

        elif pred_res == real_res:
            puntos = 1

        if usuario not in ranking:
            ranking[usuario] = 0

        ranking[usuario] += puntos

    ranking_lista = [
        {"id_usuario": user, "puntos": pts}
        for user, pts in ranking.items()
    ]

    ranking_lista.sort(key=lambda x: x["puntos"], reverse=True)

    ranking_lista = ranking_lista[offset: offset + limit]

    response = {
        "ranking": ranking_lista,
        "_links": {
            "_first": {},
            "_prev": {},
            "_next": {},
            "_last": {}
        }
    }

    return jsonify(response), 200
