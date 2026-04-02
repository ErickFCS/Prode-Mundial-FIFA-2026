

from flask import Blueprint, jsonify, request

predicciones_blueprint = Blueprint("predicciones", __name__)


@predicciones_blueprint.route("/partido/<id>/resultado", methods=["POST"])
def partidos_id_prediccion_post(id, body):
    """Registrar una predicción para un partido
    :param id: ID de partido que se utilizará en la consulta
    :type id: int
    :param prediccion: 
    :type prediccion: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'
