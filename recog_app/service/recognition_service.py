#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil
import time
from collections import Counter

import datetime

from recog_app.app import InfraLog as Ilog
from recog_app.app import app
from recog_app.constants import config_constant
from recog_app.constants import recognition_constant
from recog_app.etc.app_settings import RECOGNITION_POLLING_INTERVAL, RECOGNITION_TIMEOUT, \
    MAX_NUMBER_OF_THE_SAME_PRODUCTS
from recog_app.etc.err_code_map import ErrorCodeMap
from recog_app.lib.redis_base import RedisBase
from recog_app.utils.file_util import remove_file, is_valid_image_filename


class RecognitionService:
    def __init__(self):
        self.__rb = RedisBase()

    def post_recognition_v1(self, **params):
        from recog_app.celery_core.tasks import recognize_image

        order_id = params.get("order_id")
        order_path = params.get("order_path")
        image = params.get("image")

        # verify file extension
        raw_filename = image.filename
        if not is_valid_image_filename(raw_filename):
            return None, ErrorCodeMap.invalid_image_file_extension
        _, extension = raw_filename.rsplit(".", 1)

        # download image file
        time_info = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")  # ex. 20180118162739578037
        formatted_filename = "{}_{}.{}".format(order_id, time_info, extension)
        image_path = os.path.join(app.config[config_constant.IMAGE_FOLDER], formatted_filename)
        try:
            image.save(image_path)
        except:
            Ilog.Write(Ilog.PRI_ERROR, "[RECOGNITION FAILURE] order_id: {} download_fail")
            return None, ErrorCodeMap.download_fail

        dst_path = os.path.join(order_path, "image.{}".format(extension))
        shutil.copy(src=image_path, dst=dst_path)

        # dispatch recognition request to image_recognition queue
        recognition_task = recognize_image.delay(order_id=order_id, image_path=image_path)
        task_id = recognition_task.task_id

        # long-polling recognition result until recognition finished,
        # could avoid long-polling by passing callback url to client
        polling_duration = 0
        while True:
            raw_result = self.__rb.get_recognition_result(task_id=task_id)
            if raw_result:
                remove_file(image_path)
                recognition_result = raw_result.get("result")
                # sort recognized products by classification confidence in descending order
                recognition_result[recognition_constant.RECOGNIZED_PRODUCTS] = sorted(
                    recognition_result[recognition_constant.RECOGNIZED_PRODUCTS],
                    key=lambda k: k.get(recognition_constant.CLASSIFICATION_CONFIDENCE),
                    reverse=True
                )
                recognition_result[recognition_constant.DURATION] = polling_duration
                recognition_code = recognition_result.get(recognition_constant.RECOGNITION_CODE)
                if recognition_code != config_constant.RECOGNITION_SUCCESS_CODE:
                    Ilog.Write(Ilog.PRI_ERROR, "[RECOGNITION FAILURE] order_id: {} raw_result:{}".
                               format(order_id, raw_result))
                    return recognition_result, ErrorCodeMap.recognition_fail

                # return err code if product exceed MAX_NUMBER_OF_THE_SAME_PRODUCTS
                recognized_products = recognition_result.get(recognition_constant.RECOGNIZED_PRODUCTS)
                product_id, maximum = RecognitionService.__get_maximum_num_of_the_same_product(products=recognized_products)
                if maximum > MAX_NUMBER_OF_THE_SAME_PRODUCTS:
                    Ilog.Write(Ilog.PRI_INFO, "[Exceed MAX_NUMBER_OF_THE_SAME_PRODUCTS] "
                                              "order_id: {}, product_id: {}, num: {}".
                               format(order_id, product_id, maximum))
                    return None, ErrorCodeMap.recognition_result_exceed_max_num_of_products
                return recognition_result, ErrorCodeMap.successfully
            time.sleep(RECOGNITION_POLLING_INTERVAL)
            polling_duration += RECOGNITION_POLLING_INTERVAL

            # stop polling if recognition timeout
            if polling_duration > RECOGNITION_TIMEOUT:
                remove_file(image_path)
                return None, ErrorCodeMap.recognition_timeout

    @staticmethod
    def __get_maximum_num_of_the_same_product(products):
        product_ids = [recognized_product[config_constant.PRODUCT_ID] for recognized_product in products if config_constant.PRODUCT_ID in recognized_product]
        product_id_count_list = Counter(product_ids).most_common(1)
        if len(product_id_count_list) > 0:
            product_id, maximum = Counter(product_ids).most_common(1)[0]
            return product_id, maximum
        return None, 0
