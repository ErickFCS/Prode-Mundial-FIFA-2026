

from flask import Blueprint, jsonify, request

ranking_blueprint = Blueprint("ranking", __name__)


@ranking_blueprint.route("/ranking", methods=["GET"])
def ranking_get(limit, offset):
    """Obtener el ranking de usuarios
    :param limit: Cantidad máxima de registros que se incluirán en cada página de la respuesta.  Pueden devolverse menos registros si la consulta no produce esa cantidad.  El valor por defecto es 10.
    :type limit: int
    :param offset: Identificador de paginación que es devuelto a la aplicación por la API cuando se utilizan los enlaces HATEOAS &#39;_prev&#39; o &#39;_next&#39;.  Si no se especifica un offset, la aplicación puede navegar desde la última página devuelta hacia la siguiente, la anterior o la primera.
    :type offset: int

    :rtype: Union[RankingListResponse, Tuple[RankingListResponse, int], Tuple[RankingListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'
