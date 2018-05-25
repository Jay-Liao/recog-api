import os

from flask import Flask, Blueprint
from flask_redis import FlaskRedis
from recog_app.utils.apibase import ApiBase
from recog_app.constants.config_constant import LOG_IDENT, LOG_DEVICE, LOG_PROIORITY, LOG_PATH
from recog_app.restplus import api, app_settings, api_request_handler
from utils.infralog import InfraLog


URL_PREFIX = "/{}".format(app_settings.PROJECT_NAME)


def create_app():
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object("config")
    flask_app.config.from_pyfile("config.py", silent=True)
    flask_app.config["SWAGGER_UI_DOC_EXPANSION"] = app_settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config["RESTPLUS_VALIDATE"] = app_settings.RESTPLUS_VALIDATE
    flask_app.config["RESTPLUS_MASK_SWAGGER"] = app_settings.RESTPLUS_MASK_SWAGGER
    flask_app.config["ERROR_404_HELP"] = app_settings.RESTPLUS_ERROR_404_HELP
    flask_app.config["PROJ_BASE_DIR"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return flask_app


def initialize_app(flask_app):
    blueprint = Blueprint("api", __name__, url_prefix=URL_PREFIX)
    api.init_app(blueprint)
    flask_app.register_blueprint(blueprint)
    
app = create_app()

#########################
# external data services
#########################
redis_client = FlaskRedis(app)

from recog_app.webapi.recognition import ns as recognition_namespace
initialize_app(app)

InfraLog.Setup(
    ident=app.config[LOG_IDENT],
    device=eval(app.config[LOG_DEVICE]),
    priority=InfraLog.Priority(app.config[LOG_PROIORITY]),
    project=app.config[LOG_IDENT],
    log_path=app.config[LOG_PATH] if app.config[LOG_PATH] is not "."
    else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
api_request_handler(app, InfraLog)
