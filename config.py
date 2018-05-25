# -*-coding: utf-8 -*-
import os
import sys

from recog_app.etc.app_settings import (IMAGE_FOLDER_NAME,
                                        RECOGNITION_HISTORY_FOLDER_NAME,
                                        PROJECT_NAME)
from recog_app.utils.file_util import make_dirs

##############################
# Project
##############################
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_API_HOST = "http://127.0.0.1:8085/{}".format(PROJECT_NAME)

##############################
# redis
##############################
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_URL = "redis://{}:{}/{}".format(REDIS_HOST, REDIS_PORT, REDIS_DB)
REDIS_EXPIRE_GLOBAL = 60 * 60 * 24 * 1

##############################
# rabbitmq
##############################
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_ADMIN_PORT = 15672
RABBITMQ_USERNAME = "root"
RABBITMQ_PASSWORD = "1qaz2wsx"
RABBITMQ_URL = "amqp://{}:{}@{}:{}//".format(
    RABBITMQ_USERNAME,
    RABBITMQ_PASSWORD,
    RABBITMQ_HOST,
    RABBITMQ_PORT
)

##############################
# Logger
##############################
LOG_IDENT = PROJECT_NAME
LOG_DEVICE = "InfraLog.DEV_FILE|InfraLog.DEV_SYSLOG|InfraLog.DEV_CONSOLE "
LOG_PROIORITY = "DEBUG"
# LOG_PATH = "/opt/var/%s"%(LOG_IDENT)
LOG_PATH = "."

##############################
# Recognition
##############################
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
IMAGE_FOLDER = os.path.join(BASE_DIR, IMAGE_FOLDER_NAME)
make_dirs(IMAGE_FOLDER)

RECOGNITION_HISTORY_FOLDER = os.path.join(BASE_DIR, RECOGNITION_HISTORY_FOLDER_NAME)
make_dirs(RECOGNITION_HISTORY_FOLDER)
print >> sys.stderr, " --------------read config done, %s ----------------" % __file__
