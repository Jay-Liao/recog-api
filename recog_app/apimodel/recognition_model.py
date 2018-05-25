import werkzeug
from flask_restplus import fields, reqparse
from recog_app.app import app
from recog_app.restplus import api
from base_model import response_body
from recog_app.constants.config_constant import MAX_CONTENT_LENGTH
from recog_app.constants import response_constant
from recog_app.constants import recognition_constant

#########################
#  Request Model
#########################
post_recognition_request_v1 = reqparse.RequestParser()
post_recognition_request_v1.add_argument(
    "image", required=True, type=werkzeug.datastructures.FileStorage, location="files",
    help="image must less than {} MB".format(app.config[MAX_CONTENT_LENGTH] / (1024 * 1024))
)
post_recognition_request_v1.add_argument(
    recognition_constant.ORDER_ID, required=True, type=str, location="form",
    help="order_id of the image"
)

#########################
#  Data Model
#########################
recognized_product = api.model("recognized_product", {
    recognition_constant.PRODUCT_ID: fields.String(required=True, description="product id of the bread"),
    recognition_constant.NUM: fields.Integer(required=True, description="number of the breads"),
    recognition_constant.DETECTION_CONFIDENCE: fields.Float(required=True, description="confidence of detection"),
    recognition_constant.CLASSIFICATION_CONFIDENCE: fields.Float(required=True, description="confidence of classification"),
})

recognition_result = api.model("recognition_result", {
    recognition_constant.ORDER_ID: fields.String(required=True, description="id of the order"),
    recognition_constant.RECOGNIZED_PRODUCTS: fields.List(fields.Nested(model=recognized_product))
})

#########################
#  Response Model
#########################
post_recognition_response_v1 = api.inherit("post_recognition_response_v1", response_body, {
    response_constant.RESPONSE_DATA: fields.Nested(recognition_result)
})
