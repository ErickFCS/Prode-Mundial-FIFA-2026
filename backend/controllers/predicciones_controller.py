from flask import Blueprint, jsonify, request
from backend.db import db
import mysql.connector

predicciones_blueprint = Blueprint("predicciones", __name__)

@predicciones_blueprint.route("/partidos/<int:id>/prediccion", methods=["POST"])
def crear_prediccion(id):
    try:
        datos = request.get_json()
        id_partido = id

        if not datos:
            return jsonify(mensaje = "Se requiere el cuerpo de la predicción con los campos: id_usuario, local y visitante"), 400
        if "id_usuario" not in datos:
                return jsonify(mensaje = "Se requiere el campo 'id_usuario'"), 400
        if "local" not in datos:
                return jsonify(mensaje = "Se requiere el campo 'local'"), 400
        if "visitante" not in datos:
                return jsonify(mensaje = "Se requiere el campo 'visitante'"), 400
        
        id_usuario = datos["id_usuario"]
        goles_local = datos["local"]
        goles_visitante = datos["visitante"]

        if not isinstance(id_usuario, int):
            return jsonify(mensaje = "El campo 'id_usuario' debe ser un número entero"), 400
        if id_usuario <= 0:
            return jsonify(mensaje = "El campo 'id_usuario' debe ser un número positivo"), 400
        if not isinstance(goles_local, int):
            return jsonify(mensaje = "El campo 'local' debe ser un número entero"), 400
        if goles_local < 0:
            return jsonify(mensaje = "El campo 'local' no puede ser negativo"), 400
        if not isinstance(goles_visitante, int):
            return jsonify(mensaje = "El campo 'visitante' debe ser un número entero"), 400
        if goles_visitante < 0:
            return jsonify(mensaje = "El campo 'visitante' no puede ser negativo"), 400
        
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_partido FROM partidos WHERE id_partido = %s", (id_partido,)
        )
        partido = cursor.fetchone()

        if not partido:
            cursor.close()
            return jsonify(mensaje = f"El partido con id {id_partido} no existe."), 404
        #if partido["fecha"] < datetime.now():
            #cursor.close()
            #return jsonify(mensaje = f"No se puede predecir un partido que ya se jugó."), 409
        cursor.execute(
            "SELECT id_prediccion FROM predicciones WHERE id_usuario=%s AND id_partido=%s", (id_usuario, id_partido)
        )
        prediccion = cursor.fetchone()
        if prediccion:
            cursor.close()
            return jsonify(mensaje = f"Ya existe una predicción de este usuario para este partido."), 409
        cursor.execute(
             "INSERT INTO predicciones (id_usuario, id_partido, goles_local, goles_visitante) VALUES (%s, %s, %s, %s)",
            (id_usuario, id, goles_local, goles_visitante)
        )
        db.commit()
        cursor.close()
        return jsonify(mensaje="Predicción creada correctamente"), 201
    
    except mysql.connector.Error as err:
        db.rollback()
        return jsonify(mensaje = f"Error en la base de datos: {str(err)}"), 500
        
    except Exception as e:
        return jsonify(mensaje = f"Error interno: {str(e)}"), 500
