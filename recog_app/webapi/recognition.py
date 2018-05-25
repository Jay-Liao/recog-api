#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import datetime
from flask import request
from flask_restplus import Resource

from recog_app.apimodel.recognition_model import post_recognition_request_v1, post_recognition_response_v1
from recog_app.app import api, ApiBase
from recog_app.app import app
from recog_app.constants.config_constant import RECOGNITION_HISTORY_FOLDER
from recog_app.etc.err_code_map import ErrorCodeMap
from recog_app.service.recognition_service import RecognitionService
from recog_app.utils.file_util import make_dirs, keep_recognition_history
from recog_app.utils.flask_request_util import get_request_data

MY_FILE = os.path.basename(__file__).split(".")[0]
ns = api.namespace("webapi/{}".format(MY_FILE), description="{} Service".format(MY_FILE))

_SERVICE_ = RecognitionService()


@ns.route("/v1/image")
class Recognition(Resource, ApiBase):
    _service = _SERVICE_

    @api.expect(post_recognition_request_v1)
    @api.marshal_with(post_recognition_response_v1)
    @api.doc(description=ErrorCodeMap.get_alternatives_description(ErrorCodeMap.invalid_image_file_extension,
                                                                   ErrorCodeMap.download_fail,
                                                                   ErrorCodeMap.recognition_fail,
                                                                   ErrorCodeMap.recognition_timeout,
                                                                   ErrorCodeMap.recognition_result_exceed_max_num_of_products))
    def post(self, **kwargs):
        """ recognize image file """
        args = post_recognition_request_v1.parse_args()
        kwargs.update(args)
        order_id = kwargs.get("order_id", None)

        # makedirs - order path
        now = datetime.datetime.now()
        date_directory_name = now.strftime("%Y%m%d")  # ex. 20180118
        order_directory_name = "{}_{}".format(order_id, now.strftime("%Y%m%d%H%M%S%f"))  # ex. ID_20180118162739578037
        order_path = os.path.join(app.config[RECOGNITION_HISTORY_FOLDER], date_directory_name, order_directory_name)
        make_dirs(order_path)

        kwargs["order_path"] = order_path
        result, status_code = self.api_process(self._service.post_recognition_v1, request, **kwargs)
        request_data = get_request_data(request)
        response_data = result.copy()
        response_data["http_status_code"] = status_code
        keep_recognition_history(directory_path=order_path, request_data=request_data, response_data=response_data)
        return result, status_code
