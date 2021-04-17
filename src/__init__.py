from flask_swagger_ui import get_swaggerui_blueprint

import config

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy, get_debug_queries

app = Flask(__name__)  # Init app
app.config.from_object(config.Config)  # Configurations app
api = Api(app)  # Init api for app
db = SQLAlchemy(app)  # Init DB for app
migrate = Migrate(app, db)  # Init migrate in DB from app

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Book Library"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

# Queries debug
# app.debug = True
#
# def sql_debug(response):
#     queries = list(get_debug_queries())
#     total_dur = 0.0
#     for i in queries:
#         total_dur += i.duration
#
#     print('Queries: {} - {}'.format(len(queries), round(total_dur * 1000, 2)))
#
#     return response
#
# app.after_request(sql_debug)

from . import routes
from .database import models
