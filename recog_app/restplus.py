from flask_restplus import Api
from recog_app.etc import app_settings
from flask import Flask, request

api = Api(version="1.0", title="{} API".format(app_settings.PROJECT_NAME),
          description="{} Flask RestPlus powered API".format(app_settings.PROJECT_NAME))


def api_request_handler(app, ilg):
    
    @app.before_first_request
    def before_first_request():
        pass

    @app.before_request
    def before_request():
        ilg.Write(ilg.PRI_INFO, "**API Start : {}".format(request.url_rule))

    @app.after_request
    def after_request(response):
        ilg.Write(ilg.PRI_INFO, "**API End : {}".format(request.url_rule))
        return response
