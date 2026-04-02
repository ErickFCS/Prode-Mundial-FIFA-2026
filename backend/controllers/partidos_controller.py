

from flask import Blueprint, jsonify, request

partidos_blueprint = Blueprint("partidos", __name__)


@partidos_blueprint.route("/partidos", methods=["GET"])
def partidos_get(equipo, fecha, fase, limit, offset):
    """Listar partidos (sin resultados incluidos)
    :param equipo: Equipo que participa en el partido, ya sea como local o visitante
    :type equipo: str
    :param fecha: 
    :type fecha: str
    :param fase: 
    :type fase: dict | bytes
    :param limit: Cantidad máxima de registros que se incluirán en cada página de la respuesta.  Pueden devolverse menos registros si la consulta no produce esa cantidad.  El valor por defecto es 10.
    :type limit: int
    :param offset: Identificador de paginación que es devuelto a la aplicación por la API cuando se utilizan los enlaces HATEOAS &#39;_prev&#39; o &#39;_next&#39;.  Si no se especifica un offset, la aplicación puede navegar desde la última página devuelta hacia la siguiente, la anterior o la primera.
    :type offset: int

    :rtype: Union[PartidoListResponse, Tuple[PartidoListResponse, int], Tuple[PartidoListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


@partidos_blueprint.route("/partidos", methods=["DELETE"])
def partidos_id_delete(id):
    """Eliminar partido
    :param id: ID de partido que se utilizará en la consulta
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


@partidos_blueprint.route("/partidos", methods=["GET"])
def partidos_id_get(id):
    """Obtener un partido por ID
    :param id: ID de partido que se utilizará en la consulta
    :type id: int

    :rtype: Union[Partido, Tuple[Partido, int], Tuple[Partido, int, Dict[str, str]]
    """
    return 'do some magic!'


@partidos_blueprint.route("/partidos", methods=["PATCH"])
def partidos_id_patch(id, body):
    """Actualizar parcialmente un partido
    :param id: ID de partido que se utilizará en la consulta
    :type id: int
    :param partido_actualizacion: 
    :type partido_actualizacion: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


@partidos_blueprint.route("/partidos", methods=["PUT"])
def partidos_id_put(id, body):
    """Reemplazar un partido
    :param id: ID de partido que se utilizará en la consulta
    :type id: int
    :param partido_base: 
    :type partido_base: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


@partidos_blueprint.route("/partidos", methods=["POST"])
def partidos_post(body):
    """Crear partido
    :param partido_base: 
    :type partido_base: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'
