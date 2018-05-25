from flask_restplus import fields
from recog_app.restplus import api
from recog_app.constants import response_constant


response_body = api.model("header", {
    response_constant.API_SERVICE_VERSION: fields.String(required=True, description="version of Backery85"),
    response_constant.RESPONSE_CODE: fields.Integer(required=True, description="response code: =1 is success; <1 is fail"),
    response_constant.RESPONSE_MSG: fields.String(required=True, description="response message")
})
