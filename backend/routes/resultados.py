

from flask import Blueprint, jsonify, request

resultados_blueprint = Blueprint("resultados", __name__)


@resultados_blueprint.route("/partidos/<id>/prediccion", methods=["PUT"])
def partidos_id_resultado_put(id, body):
    """Actualizar resultado
    :param id: ID de partido que se utilizará en la consulta
    :type id: int
    :param resultado: 
    :type resultado: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'
