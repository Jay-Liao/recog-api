#!/usr/bin/python
# -*- coding: utf-8 -*-
import httplib
from app_settings import ALLOWED_IMAGE_EXTENSIONS, MAX_NUMBER_OF_THE_SAME_PRODUCTS


# err_code -100 to 100 for general case
class ErrorCodeMap(object):
    # general code
    param_error = -1
    undefined_error = -100

    successfully = 1

    successfully_exception = 2
    redis_is_unavailable = 3
    rabbitmq_is_unavailable = 4
    download_fail = 10

    # recognition code
    invalid_image_file_extension = -101
    recognition_fail = 101
    recognition_timeout = 102
    recognition_result_exceed_max_num_of_products = 103

    # version
    version_url_unavailable = 201

    @staticmethod
    def get_alternatives_description(*args):
        err_codes = list(args)
        descriptions = "\n\t\t".join([ErrorCodeMap.__get_description(err_code) for err_code in err_codes])
        return """
        Alternatives:\n\t
        {}
        """.format(descriptions)

    @staticmethod
    def __get_description(err_code):
        msg, status_code = err_map.get(err_code)
        if status_code == httplib.NO_CONTENT:
            return "status_code={}".format(httplib.NO_CONTENT)
        return """status_code={}, response_code={}, response_msg=\"{}\"""".format(status_code, err_code, msg)


# error code and msg map
err_map = { 
            ErrorCodeMap.successfully_exception: ("Successfully, Have exception", httplib.OK),
            ErrorCodeMap.successfully: ("Successfully", httplib.OK),
            ErrorCodeMap.invalid_image_file_extension: ("Only allow the following extensions: {}.".
                                                        format(ALLOWED_IMAGE_EXTENSIONS), httplib.BAD_REQUEST),
            ErrorCodeMap.recognition_result_exceed_max_num_of_products: ("Recognition result exceeds MAX_NUMBER_OF_THE_SAME_PRODUCTS: {}".
                                                                         format(MAX_NUMBER_OF_THE_SAME_PRODUCTS), httplib.OK),
            ErrorCodeMap.download_fail: ("Download fail", httplib.OK),
            ErrorCodeMap.recognition_timeout: ("Recognition is timeout", httplib.OK),
            ErrorCodeMap.recognition_fail: ("Recognition fail", httplib.OK),
            ErrorCodeMap.redis_is_unavailable: ("Redis is unavailable", httplib.OK),
            ErrorCodeMap.rabbitmq_is_unavailable: ("RabbitMQ is unavailable", httplib.OK),
            # version
            ErrorCodeMap.version_url_unavailable: ("Version URL is unavailable", httplib.OK),
            # general
            ErrorCodeMap.param_error: ("param error", httplib.BAD_REQUEST),
            ErrorCodeMap.undefined_error: ("Handle, Undefined", httplib.OK)
          }

