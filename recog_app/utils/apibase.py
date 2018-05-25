#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import traceback

from recog_app.etc.err_code_map import err_map, ErrorCodeMap
from recog_app.constants import response_constant


class ApiBase(object):
    def service_exception_handle(self, result, e=''):
        from recog_app.app import InfraLog as Ilg

        Ilg.Write(Ilg.PRI_ERROR, traceback.format_exc())
        result[response_constant.RESPONSE_MSG] = str(sys.exc_info()[0])
        result[response_constant.RESPONSE_CODE] = -99999
        return result
        
    def api_process(self, func, request, **kwargs):
        result = {}
        status_code = 200
        if request.environ["REQUEST_METHOD"] == "GET":
            params = request.view_args
        else:
            params = request.json
            if params is None:
                params = {}
        params.update(kwargs)
        try:
            result[response_constant.RESPONSE_DATA], result[response_constant.RESPONSE_CODE] = func(**params)
            (result[response_constant.RESPONSE_MSG], status_code) = err_map[ErrorCodeMap.undefined_error] if result['response_code'] not in err_map \
                else err_map[result[response_constant.RESPONSE_CODE]]
        except Exception as e:
            self.service_exception_handle(result)
        return result, status_code
