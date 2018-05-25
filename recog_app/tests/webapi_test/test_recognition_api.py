import httplib
import json
import unittest

import mock

from recog_app.app import app
from recog_app.etc.err_code_map import ErrorCodeMap
from recog_app.constants import response_constant
from recog_app.constants import recognition_constant

RECOGNITION_V1_URL = "/recog/webapi/recognition/v1/image"


class TestRecognitionApi(unittest.TestCase):
    TEST_ORDER_ID = "AUTO_TEST"

    def setUp(self):
        import io

        self.client = app.test_client()
        self.test_image = (io.BytesIO(b'test'), 'test_file.png')

    @classmethod
    def tearDownClass(cls):
        TestRecognitionApi.clean_test_recognition_histories()

    @staticmethod
    def clean_test_recognition_histories():
        import os
        import shutil
        import datetime
        from recog_app.constants import config_constant

        # clean recognition histories produced by test cases
        now = datetime.datetime.now()
        date_directory_name = now.strftime("%Y%m%d")  # ex. 20180118
        date_folder_path = os.path.join(app.config[config_constant.RECOGNITION_HISTORY_FOLDER], date_directory_name)
        folder_names = os.listdir(date_folder_path)
        for folder_name in folder_names:
            folder_path = os.path.join(date_folder_path, folder_name)
            if TestRecognitionApi.TEST_ORDER_ID in folder_name and os.path.exists(folder_path):
                shutil.rmtree(folder_path)

    def test_post_recognition_request_v1_with_txt_file(self):
        import io

        response = self.client.post(
            RECOGNITION_V1_URL,
            data=dict(
                order_id=self.TEST_ORDER_ID,
                image=(io.BytesIO(b'test'), 'test_file.txt')
            ),
            content_type='multipart/form-data'
        )
        self.assertEqual(httplib.BAD_REQUEST, response.status_code)
        response_json = json.loads(response.data)
        self.assertEqual(ErrorCodeMap.invalid_image_file_extension, response_json[response_constant.RESPONSE_CODE])

    @mock.patch("werkzeug.datastructures.FileStorage.save")
    def test_post_recognition_request_v1_when_download_fail(self, mock_save):
        mock_save.side_effect = IOError()
        response = self.client.post(
            RECOGNITION_V1_URL,
            data=dict(
                order_id=self.TEST_ORDER_ID,
                image=self.test_image
            ),
            content_type='multipart/form-data'
        )
        self.assertEqual(httplib.OK, response.status_code)
        response_json = json.loads(response.data)
        self.assertEqual(ErrorCodeMap.download_fail, response_json[response_constant.RESPONSE_CODE])

    @mock.patch("recog_app.celery_core.tasks.recognize_image.delay")
    @mock.patch("recog_app.lib.redis_base.RedisBase.get_recognition_result")
    def test_post_recognition_request_v1_when_recognition_fail(self, mock_get_recognition_result, mock_delay):
        recognition_result = {
            recognition_constant.ORDER_ID: self.TEST_ORDER_ID,
            recognition_constant.DETECTED_PRODUCTS: [],
            recognition_constant.CLASSIFIED_PRODUCTS: [],
            recognition_constant.RECOGNIZED_PRODUCTS: [],
            recognition_constant.RECOGNITION_CODE: -9999,
            recognition_constant.RECOGNITION_MSG: "fail"
        }

        mock_get_recognition_result.return_value = dict(result=recognition_result)
        mock_delay.side_effect = None
        response = self.client.post(
            RECOGNITION_V1_URL,
            data=dict(
                order_id=self.TEST_ORDER_ID,
                image=self.test_image
            ),
            content_type='multipart/form-data'
        )
        self.assertEqual(httplib.OK, response.status_code)
        response_json = json.loads(response.data)
        self.assertEqual(ErrorCodeMap.recognition_fail, response_json[response_constant.RESPONSE_CODE])
        response_data = response_json[response_constant.RESPONSE_DATA]
        self.assertEqual(recognition_result[recognition_constant.ORDER_ID], response_data[recognition_constant.ORDER_ID])
        self.assertEqual(recognition_result[recognition_constant.RECOGNIZED_PRODUCTS], response_data[recognition_constant.RECOGNIZED_PRODUCTS])

    @mock.patch("time.sleep")
    @mock.patch("recog_app.celery_core.tasks.recognize_image.delay")
    @mock.patch("recog_app.lib.redis_base.RedisBase.get_recognition_result")
    def test_post_recognition_request_v1_when_recognition_timeout(self, mock_get_recognition_result, mock_delay,
                                                                  mock_sleep):
        mock_sleep.side_effect = None
        mock_get_recognition_result.return_value = None
        mock_delay.side_effect = None
        response = self.client.post(
            RECOGNITION_V1_URL,
            data=dict(
                order_id=self.TEST_ORDER_ID,
                image=self.test_image
            ),
            content_type='multipart/form-data'
        )
        self.assertEqual(httplib.OK, response.status_code)
        response_json = json.loads(response.data)
        self.assertEqual(ErrorCodeMap.recognition_timeout, response_json[response_constant.RESPONSE_CODE])

    @mock.patch("recog_app.celery_core.tasks.recognize_image.delay")
    @mock.patch("recog_app.lib.redis_base.RedisBase.get_recognition_result")
    def test_post_recognition_request_v1_when_recognition_result_exceed_max_num_of_products(self, mock_get_recognition_result, mock_delay):
        from recog_app.etc.app_settings import MAX_NUMBER_OF_THE_SAME_PRODUCTS

        recognized_product = {
            recognition_constant.PRODUCT_ID: "bread01",
            recognition_constant.NUM: 1,
            recognition_constant.DETECTION_CONFIDENCE: 0.99,
            recognition_constant.CLASSIFICATION_CONFIDENCE: 0.75,
            recognition_constant.LOCATION: {
                recognition_constant.X: 1,
                recognition_constant.Y: 2,
                recognition_constant.W: 400,
                recognition_constant.H: 400
            }
        }
        recognized_products = list()
        exceed_max_number_of_the_same_products = MAX_NUMBER_OF_THE_SAME_PRODUCTS + 1
        for i in range(exceed_max_number_of_the_same_products):
            recognized_products.append(recognized_product)
        recognition_result = {
            recognition_constant.ORDER_ID: self.TEST_ORDER_ID,
            recognition_constant.DETECTED_PRODUCTS: [],
            recognition_constant.CLASSIFIED_PRODUCTS: [],
            recognition_constant.RECOGNIZED_PRODUCTS: recognized_products,
            recognition_constant.RECOGNITION_CODE: 0,
            recognition_constant.RECOGNITION_MSG: "success"
        }
        mock_get_recognition_result.return_value = dict(result=recognition_result)
        mock_delay.side_effect = None
        response = self.client.post(
            RECOGNITION_V1_URL,
            data=dict(
                order_id=self.TEST_ORDER_ID,
                image=self.test_image
            ),
            content_type='multipart/form-data'
        )
        self.assertEqual(httplib.OK, response.status_code)
        response_json = json.loads(response.data)
        self.assertEqual(ErrorCodeMap.recognition_result_exceed_max_num_of_products, response_json[response_constant.RESPONSE_CODE])

    @mock.patch("recog_app.celery_core.tasks.recognize_image.delay")
    @mock.patch("recog_app.lib.redis_base.RedisBase.get_recognition_result")
    def test_post_recognition_request_v1_when_recognition_successfully(self, mock_get_recognition_result, mock_delay):
        recognized_products = [{
            recognition_constant.PRODUCT_ID: "bread01",
            recognition_constant.NUM: 1,
            recognition_constant.DETECTION_CONFIDENCE: 0.75,
            recognition_constant.CLASSIFICATION_CONFIDENCE: 0.85,
            recognition_constant.LOCATION: {
                recognition_constant.X: 1,
                recognition_constant.Y: 2,
                recognition_constant.W: 400,
                recognition_constant.H: 400
            }
        }, {
            recognition_constant.PRODUCT_ID: "bread01",
            recognition_constant.NUM: 1,
            recognition_constant.DETECTION_CONFIDENCE: 0.75,
            recognition_constant.CLASSIFICATION_CONFIDENCE: 0.91,
            recognition_constant.LOCATION: {
                recognition_constant.X: 1,
                recognition_constant.Y: 2,
                recognition_constant.W: 400,
                recognition_constant.H: 400
            }
        }, {
            recognition_constant.PRODUCT_ID: "bread02",
            recognition_constant.NUM: 1,
            recognition_constant.DETECTION_CONFIDENCE: 0.75,
            recognition_constant.CLASSIFICATION_CONFIDENCE: 0.99,
            recognition_constant.LOCATION: {
                recognition_constant.X: 1,
                recognition_constant.Y: 2,
                recognition_constant.W: 400,
                recognition_constant.H: 400
            }
        }]
        recognition_result = {
            recognition_constant.ORDER_ID: self.TEST_ORDER_ID,
            recognition_constant.DETECTED_PRODUCTS: [],
            recognition_constant.CLASSIFIED_PRODUCTS: [],
            recognition_constant.RECOGNIZED_PRODUCTS: recognized_products,
            recognition_constant.RECOGNITION_CODE: 0,
            recognition_constant.RECOGNITION_MSG: "success"
        }
        mock_get_recognition_result.return_value = dict(result=recognition_result)
        mock_delay.side_effect = None
        response = self.client.post(
            RECOGNITION_V1_URL,
            data=dict(
                order_id=self.TEST_ORDER_ID,
                image=self.test_image
            ),
            content_type='multipart/form-data'
        )
        self.maxDiff = None
        self.assertEqual(httplib.OK, response.status_code)
        response_json = json.loads(response.data)
        self.assertEqual(ErrorCodeMap.successfully, response_json[response_constant.RESPONSE_CODE])
        for recognized_product in recognized_products:
            recognized_product.pop(recognition_constant.LOCATION, None)
        response_data = response_json[response_constant.RESPONSE_DATA]
        self.assertEqual(self.TEST_ORDER_ID, response_data[recognition_constant.ORDER_ID])
        self.assertDictEqual(recognized_products[2], response_data[recognition_constant.RECOGNIZED_PRODUCTS][0])
        self.assertDictEqual(recognized_products[1], response_data[recognition_constant.RECOGNIZED_PRODUCTS][1])
        self.assertDictEqual(recognized_products[0], response_data[recognition_constant.RECOGNIZED_PRODUCTS][2])

    @mock.patch("recog_app.celery_core.tasks.recognize_image.delay")
    @mock.patch("recog_app.lib.redis_base.RedisBase.get_recognition_result")
    def test_post_recognition_request_v1_when_no_recognition_result(self, mock_get_recognition_result, mock_delay):
        recognition_result = {
            recognition_constant.ORDER_ID: self.TEST_ORDER_ID,
            recognition_constant.DETECTED_PRODUCTS: [],
            recognition_constant.CLASSIFIED_PRODUCTS: [],
            recognition_constant.RECOGNIZED_PRODUCTS: [],
            recognition_constant.RECOGNITION_CODE: 0,
            recognition_constant.RECOGNITION_MSG: "success"
        }
        mock_get_recognition_result.return_value = dict(result=recognition_result)
        mock_delay.side_effect = None
        response = self.client.post(
            RECOGNITION_V1_URL,
            data=dict(
                order_id=self.TEST_ORDER_ID,
                image=self.test_image
            ),
            content_type='multipart/form-data'
        )
        self.assertEqual(httplib.OK, response.status_code)
        response_json = json.loads(response.data)
        self.assertEqual(ErrorCodeMap.successfully, response_json[response_constant.RESPONSE_CODE])
        response_data = response_json[response_constant.RESPONSE_DATA]
        self.assertEqual(recognition_result[recognition_constant.ORDER_ID], response_data[recognition_constant.ORDER_ID])
        self.assertEqual(recognition_result[recognition_constant.RECOGNIZED_PRODUCTS], response_data[recognition_constant.RECOGNIZED_PRODUCTS])
