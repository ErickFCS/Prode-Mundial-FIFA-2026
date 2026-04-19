#!./.venv/bin/python

from flasgger.base import yaml
from flask import Flask, jsonify
from flasgger import Swagger

from backend.routes.partidos import partidos_blueprint
from backend.routes.predicciones import predicciones_blueprint
from backend.routes.ranking import ranking_blueprint
from backend.routes.resultados import resultados_blueprint
from backend.routes.usuarios import usuarios_blueprint
from backend.utils import INTERNAL_ERROR_CODE

app = Flask(__name__)

with open("./swagger.yaml", "r") as f:
    swagger_file = yaml.safe_load(f.read())
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "openapi": "3.0.0",
}
swagger = Swagger(app, config=swagger_config, template=swagger_file)


@app.route("/ping", methods=["GET"])
def pong():
    return "pong", 200


app.register_blueprint(partidos_blueprint)
app.register_blueprint(predicciones_blueprint)
app.register_blueprint(ranking_blueprint)
app.register_blueprint(resultados_blueprint)
app.register_blueprint(usuarios_blueprint)


@app.errorhandler(Exception)
def manejar_errores(error_crudo):

    print(error_crudo)

    error_por_defecto = {
        "code": 500,
        "description": "INTERNAL SERVER ERROR",
        "level": "error",
        "message": "Error desconocido",
    }
    errores = error_crudo.args[0] if error_crudo.args else [error_por_defecto]

    try:
        return jsonify(errores), errores[0].get("code", INTERNAL_ERROR_CODE)
    except Exception as error_desconocido:
        error_por_defecto.update({"message": str(error_desconocido)})
        return jsonify([error_por_defecto]), INTERNAL_ERROR_CODE


if __name__ == "__main__":
    app.run(debug=True)
