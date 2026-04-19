#!./.venv/bin/python

import traceback

from flasgger.base import yaml
from flask import Flask, jsonify
from flasgger import Swagger
from werkzeug.exceptions import HTTPException

from backend.routes.partidos import partidos_blueprint
from backend.routes.predicciones import predicciones_blueprint
from backend.routes.ranking import ranking_blueprint
from backend.routes.resultados import resultados_blueprint
from backend.routes.usuarios import usuarios_blueprint
from backend.utils import (
    INTERNAL_ERROR_CODE,
    INTERNAL_ERROR_CODE_MESSAGE,
    OK_CODE,
)

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
    return "pong", OK_CODE


app.register_blueprint(partidos_blueprint)
app.register_blueprint(predicciones_blueprint)
app.register_blueprint(ranking_blueprint)
app.register_blueprint(resultados_blueprint)
app.register_blueprint(usuarios_blueprint)


@app.errorhandler(HTTPException)
def manejar_errores_nativos(error_crudo):
    error = {
        "code": error_crudo.code,
        "description": error_crudo.description,
        "level": "error",
        "message": "Error nativo",
    }

    return jsonify(errors=[error]), error_crudo.code


@app.errorhandler(Exception)
def manejar_errores(error_crudo):
    traceback.print_exc()

    es_error_personal = (
        isinstance(error_crudo, RuntimeError)
        and error_crudo.args
        and isinstance(error_crudo.args[0], list)
    )

    errors = []

    if es_error_personal:
        errors = error_crudo.args[0]
        if len(errors) == 0:
            errors = [
                {
                    "code": INTERNAL_ERROR_CODE,
                    "description": INTERNAL_ERROR_CODE_MESSAGE,
                    "level": "error",
                    "message": "Se lanzo un error personal, pero vacio.",
                }
            ]

    else:
        errors = [
            {
                "code": INTERNAL_ERROR_CODE,
                "description": INTERNAL_ERROR_CODE_MESSAGE,
                "level": "error",
                "message": "Error desconocido. Valla a la consola para más información",
            }
        ]

    codigo_http = errors[0].get("code")

    return jsonify(errors=errors), codigo_http


if __name__ == "__main__":
    app.run(debug=True)
