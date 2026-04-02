

from flask import Blueprint, jsonify, request

usuarios_blueprint = Blueprint("usuarios", __name__)


@usuarios_blueprint.route("/usuarios", methods=["GET"])
def usuarios_get(limit, offset):
    """Listar usuarios
    :param limit: Cantidad máxima de registros que se incluirán en cada página de la respuesta.  Pueden devolverse menos registros si la consulta no produce esa cantidad.  El valor por defecto es 10.
    :type limit: int
    :param offset: Identificador de paginación que es devuelto a la aplicación por la API cuando se utilizan los enlaces HATEOAS &#39;_prev&#39; o &#39;_next&#39;.  Si no se especifica un offset, la aplicación puede navegar desde la última página devuelta hacia la siguiente, la anterior o la primera.
    :type offset: int

    :rtype: Union[UsuarioListResponse, Tuple[UsuarioListResponse, int], Tuple[UsuarioListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


@usuarios_blueprint.route("/usuarios", methods=["DELETE"])
def usuarios_id_delete(id):
    """Eliminar usuario
    :param id: ID de usuario que se utilizará en la consulta
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


@usuarios_blueprint.route("/usuarios", methods=["GET"])
def usuarios_id_get(id):
    """Obtener un usuario por ID
    :param id: ID de usuario que se utilizará en la consulta
    :type id: int

    :rtype: Union[Usuario, Tuple[Usuario, int], Tuple[Usuario, int, Dict[str, str]]
    """
    return 'do some magic!'


@usuarios_blueprint.route("/usuarios", methods=["PUT"])
def usuarios_id_put(id, body):
    """Reemplazar un usuario
    Reemplaza todos los campos de un usuario existente. Si no existe, lo crea. Todos los campos son obligatorios.

    :param id: ID de usuario que se utilizará en la consulta
    :type id: int
    :param usuario_base: 
    :type usuario_base: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


@usuarios_blueprint.route("/usuarios", methods=["POST"])
def usuarios_post(body):
    """Crear usuario
    :param usuario_base: 
    :type usuario_base: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'
