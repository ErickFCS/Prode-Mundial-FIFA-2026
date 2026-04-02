#!../.venv/bin/python

from flask import Flask

from controllers.partidos_controller import partidos_blueprint
from controllers.predicciones_controller import predicciones_blueprint
from controllers.ranking_controller import ranking_blueprint
from controllers.resultados_controller import resultados_blueprint
from controllers.usuarios_controller import usuarios_blueprint

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def pong():
    return "pong", 200

app.register_blueprint(partidos_blueprint)
app.register_blueprint(predicciones_blueprint)
app.register_blueprint(ranking_blueprint)
app.register_blueprint(resultados_blueprint)
app.register_blueprint(usuarios_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
