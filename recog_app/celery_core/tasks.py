import time

from celery import Celery

import image_recognition_config
from recog_app.constants.config_constant import RECOGNITION_SUCCESS_CODE

#####################################
# init celery app - image_recognition_app
#####################################
image_recognition_app = Celery()
image_recognition_app.config_from_object(image_recognition_config)


@image_recognition_app.task(name=image_recognition_app.conf["IMAGE_RECOGNITION_TASK_NAME"], acks_late=True)
def recognize_image(order_id, image_path):
    # TODO: wait for recognizing
    time.sleep(1)

    # detection threshold = 0.9
    detected_products = [dict(detection_confidence=0.7, location=dict(x=1, y=2, w=400, h=400)),
                         dict(detection_confidence=0.6, location=dict(x=1, y=2, w=400, h=400)),
                         dict(detection_confidence=0.75, location=dict(x=1, y=2, w=400, h=400))]

    # classification threshold = 0.8
    classified_products = [dict(product_id="bread01", num=1, detection_confidence=0.91, classification_confidence=0.75,
                                location=dict(x=1, y=2, w=400, h=400)),
                           dict(product_id="bread01", num=1, detection_confidence=0.85, classification_confidence=0.66,
                                location=dict(x=1, y=2, w=400, h=400)),
                           dict(product_id="bread02", num=1, detection_confidence=0.95, classification_confidence=0.25,
                                location=dict(x=1, y=2, w=400, h=400))]

    # recognized products

    recognized_products = [dict(product_id="bread01", num=1, detection_confidence=0.99, classification_confidence=0.85,
                                location=dict(x=1, y=2, w=400, h=400)),
                           dict(product_id="bread01", num=1, detection_confidence=0.98, classification_confidence=0.88,
                                location=dict(x=1, y=2, w=400, h=400)),
                           dict(product_id="bread02", num=1, detection_confidence=0.96, classification_confidence=0.91,
                                location=dict(x=1, y=2, w=400, h=400))]
    dup_recognized_product = dict(product_id="bread03", num=1, detection_confidence=0.96,
                                  classification_confidence=0.82,
                                  location=dict(x=1, y=2, w=400, h=400))
    for i in range(10):
        recognized_products.append(dup_recognized_product)
    recognition_result = dict(
        order_id=order_id,
        detected_products=detected_products,
        classified_products=classified_products,
        recognized_products=recognized_products,
        recognition_code=RECOGNITION_SUCCESS_CODE,
        recognition_msg="success"
    )
    return recognition_result
