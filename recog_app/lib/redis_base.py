#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from recog_app.app import redis_client, app
from recog_app.utils.serializer import serialize_dict


class RedisBase:
    def __init__(self):
        self.__recognition_result_key = "celery-task-meta-{}"

    def __set(self, redis_key, value_obj, expire=app.config["REDIS_EXPIRE_GLOBAL"]):
        value_obj = serialize_dict(value_obj)
        redis_client.set(redis_key, json.dumps(value_obj), ex=expire)

    def __get(self, redis_key):
        cache_str = redis_client.get(redis_key)
        if cache_str:
            cache_obj = json.loads(cache_str)
            return cache_obj

    def __del(self, redis_key):
        redis_client.delete(redis_key)
        return True

    def get_recognition_result(self, task_id):
        redis_key = self.__recognition_result_key.format(task_id)
        return self.__get(redis_key=redis_key)

    def remove_recognition_result(self, task_id):
        redis_key = self.__recognition_result_key.format(task_id)
        self.__del(redis_key=redis_key)

    # lock / unlock
    def lock(self, redis_key, expire=60 * 3):
        return redis_client.set(redis_key, 1, nx=True, ex=expire)

    def unlock(self, redis_key):
        redis_client.delete(redis_key)
