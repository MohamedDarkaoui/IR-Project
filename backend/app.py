from flask import Flask
from flask_restful import Api
from backend.src.resources.api import init
from flasgger import Swagger



def create_app(config_name="development"):
    app = Flask(__name__)
    api = Api(app)
    init(api)
    swag = Swagger(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)